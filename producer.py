import asyncio
import logging

import orjson
from aio_pika import connect, ExchangeType, Message

import configparser
import sys
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")

logger = logging.getLogger(__name__)

SECOND = 1
MINUTE = 60
TEN_MINUTES = MINUTE * 10
HOUR = MINUTE * 60
DAY = HOUR * 24

periodic_tasks = [
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_orders',
            'routing_key': 'logger.periodic.check_orders',
            'interval': MINUTE,
            'delay': SECOND * 30,
            'payload': {}
        },
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_and_update_arbitrage_possibilities',
            'routing_key': 'logger.periodic.check_and_update_arbitrage_possibilities',
            'interval': SECOND * 5,
            'delay': SECOND * 5,
            'payload': {}
        },
        {
            'exchange': 'logger.periodic',
            'queue': 'logger.periodic.check_and_update_disbalances',
            'routing_key': 'logger.periodic.check_and_update_disbalances',
            'interval': SECOND * 5,
            'delay': SECOND * 5,
            'payload': {}
        }
    ]


class WorkerProducer:
    def __init__(self, loop):
        self.loop = loop
        rabbit = config['RABBIT']
        self.rabbit_url = f"amqp://{rabbit['USERNAME']}:{rabbit['PASSWORD']}@{rabbit['HOST']}:{rabbit['PORT']}/"
        self.periodic_tasks = []

    async def run(self):
        for task in periodic_tasks:
            self.periodic_tasks.append(self.loop.create_task(self._publishing_task(task)))

    async def _publishing_task(self, task):
        if task['delay']:
            await asyncio.sleep(task['delay'])

        while True:
            connection = await connect(url=self.rabbit_url, loop=self.loop)

            channel = await connection.channel()

            exchange = await channel.declare_exchange(task['exchange'], type=ExchangeType.DIRECT, durable=True)
            queue = await channel.declare_queue(task['queue'], durable=True)
            await queue.bind(exchange, routing_key=task['routing_key'])

            message = Message(orjson.dumps(task['payload']) if task.get('payload') else b'{}')
            await exchange.publish(message, routing_key=task['routing_key'])

            logger.info(f'Published message to queue {task["queue"]}')

            await connection.close()

            await asyncio.sleep(task['interval'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    worker = WorkerProducer(loop)
    loop.run_until_complete(worker.run())

    try:
        loop.run_forever()
    finally:
        loop.close()
