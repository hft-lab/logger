import asyncio
import logging

import orjson
from aio_pika import connect, ExchangeType, Message

from config import Config

logger = logging.getLogger(__name__)


class WorkerProducer:
    def __init__(self, loop):
        self.loop = loop
        self.rabbit_url = f"amqp://{Config.RABBIT['username']}:{Config.RABBIT['password']}@{Config.RABBIT['host']}:{Config.RABBIT['port']}/"
        self.periodic_tasks = []

    async def run(self):
        for task in Config.PERIODIC_TASKS:
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
