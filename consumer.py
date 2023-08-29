import argparse
import asyncio
import logging
import traceback
from logging.config import dictConfig

import asyncpg
import orjson
from aio_pika import connect_robust
from aiohttp.web import Application

from tasks.event.insert_to_arbitrage_possibilities import InsertToArbitragePossibilities
from tasks.event.insert_to_balance_detalization import InsertToBalanceDetalization
from tasks.event.insert_to_balance_jumps import InsertToBalanceJumps
from tasks.event.insert_to_balances import InsertToBalances
from tasks.event.insert_to_disbalances import InsertToDisbalance
from tasks.event.insert_to_fundings import InsertFunding
from tasks.event.insert_to_orders import InsertToOrders
from tasks.event.insert_to_ping_logger import InsertToPingLogging
from tasks.event.send_to_telegram import Telegram
from tasks.event.update_orders import UpdateOrders
from tasks.event.update_to_bot_launches import UpdateBotLaunches
from tasks.periodic.check_and_update_arbitrage_possibilities import CheckAndUpdateArbitragePossibilities
from tasks.periodic.check_and_update_disbalances import CheckAndUpdateDisbalances
from tasks.periodic.check_orders import CheckOrders

import configparser
import sys
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")

dictConfig({'version': 1, 'disable_existing_loggers': False, 'formatters': {
                'simple': {'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'}},
            'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple',
                'stream': 'ext://sys.stdout'}},
            'loggers': {'': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False}}})
logger = logging.getLogger(__name__)

TASKS = {
    'logger.event.insert_ping_logger': InsertToPingLogging,
    'logger.event.send_to_telegram': Telegram,
    'logger.event.insert_balance_jumps': InsertToBalanceJumps,

    # NEW ------------------------------------------------------------------------
    'logger.event.insert_arbitrage_possibilities': InsertToArbitragePossibilities,
    'logger.event.insert_orders': InsertToOrders,
    'logger.event.insert_balances': InsertToBalances,
    'logger.event.insert_balance_detalization': InsertToBalanceDetalization,
    'logger.event.insert_disbalances': InsertToDisbalance,
    'logger.event.update_orders': UpdateOrders,
    'logger.event.insert_funding': InsertFunding,
    'logger.event.update_bot_launches': UpdateBotLaunches,

    'logger.periodic.check_and_update_arbitrage_possibilities': CheckAndUpdateArbitragePossibilities,
    'logger.periodic.check_and_update_disbalances': CheckAndUpdateDisbalances,
    'logger.periodic.check_orders': CheckOrders
}


class Consumer:
    """
    Producer get periodic and events tasks from RabbitMQ
    """

    def __init__(self, loop, queue=None):
        self.app = Application()
        self.loop = loop
        self.queue = queue
        rabbit = config['RABBIT']
        self.rabbit_url = f"amqp://{rabbit['USERNAME']}:{rabbit['PASSWORD']}@{rabbit['HOST']}:{rabbit['PORT']}/"
        self.periodic_tasks = []

    async def run(self) -> None:
        """
        Init setup db connection and star tasks from queue
        :return: None
        """
        await self.setup_db()
        await self.setup_mq()

        logger.info(f"Queue: {self.queue}")
        logger.info(f"Exist queue: {self.queue in TASKS}")

        if self.queue and self.queue in TASKS:
            logger.info("Single work option")
            self.periodic_tasks.append(self.loop.create_task(self._consume(self.app['mq'], self.queue)))

    async def setup_db(self) -> None:
        self.app['db'] = await asyncpg.create_pool(**{'database': config['POSTGRES']['NAME'],
                                                      'user': config['POSTGRES']['USER'],
                                                      'password': config['POSTGRES']['PASSWORD'],
                                                      'host': config['POSTGRES']['HOST'],
                                                      'port': config['POSTGRES']['PORT'],
                                                      }
                                                   )

    async def setup_mq(self):
        self.app['mq'] = await connect_robust(self.rabbit_url, loop=self.loop)

    async def _consume(self, connection, queue_name) -> None:
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(self.on_message)

    async def on_message(self, message) -> None:
        logger.info(f"\n\nReceived message {message.routing_key}")
        try:
            if 'logger.periodic' in message.routing_key:
                await message.ack()
            task = TASKS.get(message.routing_key)(self.app)
            await task.run(orjson.loads(message.body))
            logger.info(f"Success task {message.routing_key}")
            if 'logger.event' in message.routing_key:
                await message.ack()
        except Exception as e:
            logger.info(f"Error {e} while serving task {message.routing_key}")
            traceback.print_exc()
            await message.ack()


if __name__ == '__main__':
    queues = [config['QUEUES'][y] for y in config['QUEUES']]
    for queue in queues:
        loop = asyncio.get_event_loop()
        workers = [Consumer(loop, queue=q).run() for q in queues]

        # Run all workers concurrently
        loop.run_until_complete(asyncio.gather(*workers))

        try:
            loop.run_forever()
        finally:
            loop.close()
