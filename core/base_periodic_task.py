import asyncio

import asyncpg
from aio_pika import connect_robust

from config import Config
from core.rabbit_mq import publish_message


class BasePeriodicTask:
    """
    Base class for periodic tasks
    """

    EXCHANGE_NAME = None
    ROUTING_KEY = None
    QUEUE_NAME = None

    def __init__(self):
        self.db = None
        self.mq = None
        self.data = None

        self.rabbit_url = f"amqp://{Config.RABBIT['username']}:{Config.RABBIT['password']}@{Config.RABBIT['host']}:{Config.RABBIT['port']}/"  # noqa

    async def run(self) -> None:
        """
        Run setup connections to  postgresql, rabbitmq
        Getting data and prepare data for message
        Send message to rabbitmq
        :return:
        """
        await self.connect_db()
        await self.connect_mq()
        await self.get_data()
        await self.prepare_message()
        await self.send_to_rabbit()

    async def connect_db(self) -> None:
        self.db = await asyncpg.create_pool(**Config.POSTGRES)

    async def connect_mq(self) -> None:
        loop = asyncio.get_event_loop()
        self.db = await connect_robust(self.rabbit_url, loop=loop)

    async def send_to_rabbit(self):
        await publish_message(
            connection=self.mq,
            message=self.data,
            exchange_name=self.EXCHANGE_NAME,
            routing_key=self.ROUTING_KEY,
            queue_name=self.QUEUE_NAME,
        )

    async def prepare_message(self):
        raise Exception('Method not implemented')

    async def get_data(self):
        raise Exception('Method not implemented')
