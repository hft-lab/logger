import argparse
import asyncio
import logging
import traceback
from logging.config import dictConfig

import asyncpg
import orjson
from aio_pika import connect_robust
from aiohttp.web import Application

from config import Config
from tasks.periodic.check_and_update_disbalances import CheckAndUpdateDisbalances
from tasks.periodic.check_and_update_arbitrage_possibilities import CheckAndUpdateArbitragePossibilities
from tasks.periodic.check_orders import CheckOrders
from tasks.event.insert_to_fundings import InsertFunding
from tasks.event.insert_to_arbitrage_possibilities import InsertToArbitragePossibilities
from tasks.event.insert_to_balance_check import InsertToBalanceCheck
from tasks.event.insert_to_balance_detalization import InsertToBalanceDetalization
from tasks.event.insert_to_balance_jumps import InsertToBalanceJumps
from tasks.event.insert_to_balances import InsertToBalances
from tasks.event.insert_to_balancing_reports import InsertToBalancingReports
from tasks.event.insert_to_deals_reports import InsertToDealsReports
from tasks.event.insert_to_disbalances import InsertToDisbalance
from tasks.event.insert_to_orders import InsertToOrders
from tasks.event.insert_to_ping_logger import InsertToPingLogging
from tasks.event.send_to_telegram import Telegram
from tasks.event.update_orders import UpdateOrders

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)

TASKS = {
    'logger.event.insert_ping_logger': InsertToPingLogging,
    'logger.event.send_to_telegram': Telegram,
    'logger.event.insert_balance_jumps': InsertToBalanceJumps,
    'logger.event.insert_deals_reports': InsertToDealsReports,
    'logger.event.insert_balance_check': InsertToBalanceCheck,
    'logger.event.insert_balancing_reports': InsertToBalancingReports,

    # NEW ------------------------------------------------------------------------
    'logger.event.insert_arbitrage_possibilities': InsertToArbitragePossibilities,
    'logger.event.insert_orders': InsertToOrders,
    'logger.event.insert_balances': InsertToBalances,
    'logger.event.insert_balance_detalization': InsertToBalanceDetalization,
    'logger.event.insert_disbalances': InsertToDisbalance,
    'logger.event.update_orders': UpdateOrders,
    'logger.event.insert_funding': InsertFunding

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
        self.rabbit_url = f"amqp://{Config.RABBIT['username']}:{Config.RABBIT['password']}@{Config.RABBIT['host']}:{Config.RABBIT['port']}/"  # noqa
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

        else:
            logger.info("Multiple work option")
            for queue_name in TASKS:
                self.periodic_tasks.append(self.loop.create_task(self._consume(self.app['mq'], queue_name)))

    async def setup_db(self) -> None:
        self.app['db'] = await asyncpg.create_pool(**Config.POSTGRES)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', nargs='?', const=True, dest='queue', default='logger.event.insert_funding')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    worker = Consumer(loop, queue=args.queue.strip())
    loop.run_until_complete(worker.run())

    try:
        loop.run_forever()
    finally:
        loop.close()
