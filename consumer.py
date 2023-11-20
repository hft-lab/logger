import asyncio
import logging
import traceback
from logging.config import dictConfig

import asyncpg
import orjson
from aio_pika import connect_robust
from aiohttp.web import Application

from tasks.all_tasks import QUEUES_TASKS

import configparser
import sys
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")

setts = config['RABBIT']
RABBIT_URL = f"amqp://{setts['USERNAME']}:{setts['PASSWORD']}@{setts['HOST']}:{setts['PORT']}/"

setts = config['POSTGRES']
POSTGRES = {'database': setts['NAME'],'user': setts['USER'],'password': setts['PASSWORD'],
            'host': setts['HOST'],'port': setts['PORT'],}

dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False}}})
logger = logging.getLogger(__name__)

class Consumer:
    """
    Consumer gets periodic and events tasks from RabbitMQ
    """

    def __init__(self, loop, queue=None):
        self.app = Application()
        self.loop = loop
        self.queue = queue
        self.rabbit_url = RABBIT_URL
        self.postgres = POSTGRES


    async def run(self) -> None:
        """
        Init setup db connection and start getting tasks from queue
        :return: None
        """
        self.app['db'] = await asyncpg.create_pool(**self.postgres)
        self.app['mq'] = await connect_robust(self.rabbit_url, loop=self.loop)

        logger.info(f"Queue: {self.queue}")
        logger.info(f"Exist queue: {self.queue in QUEUES_TASKS}")

        self.loop.create_task(self._consume(self.app['mq'], self.queue))


    async def _consume(self, connection, queue_name) -> None:
        print(f"RUN CONSUMER FOR {queue_name}")
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(self.on_message)

    async def on_message(self, message) -> None:
        logger.info(f"\n\nReceived message\n{message.routing_key=}\n{message.body=}")
        try:
            if any(keyword in message.routing_key for keyword in ['logger.periodic', 'logger.event']):
                await message.ack()
            # TBD. Принтануть message в telegram, чтобы посмотреть формат
            task = QUEUES_TASKS.get(message.routing_key)(self.app)
            await task.run(orjson.loads(message.body))
            logger.info(f"Success task {message.routing_key}")

        except Exception as e:
            logger.info(f"Error {e} while serving task {message.routing_key}")
            traceback.print_exc()
            await message.ack()


if __name__ == '__main__':
    queues = list(QUEUES_TASKS.keys())
    loop = asyncio.get_event_loop()
    workers = [Consumer(loop, queue=q).run() for q in queues]
    # Run all workers concurrently
    loop.run_until_complete(asyncio.gather(*workers))

    try:
        loop.run_forever()
    finally:
        loop.close()
