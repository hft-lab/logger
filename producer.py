import asyncio
import logging

import orjson
from aio_pika import connect, ExchangeType, Message

from telegram_for_debug import Telegram
from config import Config

logger = logging.getLogger(__name__)

periodic_tasks = Config.PERIODIC_TASKS


class WorkerProducer:
    def __init__(self, loop):
        self.loop = loop
        self.rabbit_url = Config.RABBIT_URL
        self.periodic_tasks = []
        self.telegram = Telegram()

    async def run(self):
        for task in periodic_tasks:
            self.periodic_tasks.append(self.loop.create_task(self._publishing_task(task)))


    async def _publishing_task_new(self, task):
        await asyncio.sleep(task.get('delay', 0))
        try:
            async with connect(url=self.rabbit_url, loop=self.loop) as connection:
                channel = await connection.channel()

                exchange = await channel.declare_exchange(task['exchange'], type=ExchangeType.DIRECT, durable=True)
                queue = await channel.declare_queue(task['queue'], durable=True)
                await queue.bind(exchange, routing_key=task['routing_key'])

                while True:

                    message = Message(orjson.dumps(task.get('payload', {})))
                    await exchange.publish(message, routing_key=task['routing_key'])

                    logger.info(f'Published message to queue {task["queue"]}')

                    await asyncio.sleep(task['interval'])
        except Exception as e:
            logger.error(f'Error in _publishing_task: {e}')

    async def _publishing_task(self, task):
        await asyncio.sleep(task.get('delay', 0))

        while True:
            connection = await connect(url=self.rabbit_url, loop=self.loop)
            channel = await connection.channel()

            exchange = await channel.declare_exchange(task['exchange'], type=ExchangeType.DIRECT, durable=True)
            queue = await channel.declare_queue(task['queue'], durable=True)
            await queue.bind(exchange, routing_key=task['routing_key'])

            message = Message(orjson.dumps(task.get('payload', {})))
            await exchange.publish(message, routing_key=task['routing_key'])

            logger.info(f'Published message to queue {task["queue"]}')

            await connection.close()

            await asyncio.sleep(task['interval'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    worker = WorkerProducer(loop)
    print(worker.rabbit_url)
    worker.telegram.send_message("Dima")
    loop.run_until_complete(worker.run())
    worker.telegram.send_message("Run Until Complete Finished" + str(worker.periodic_tasks))
    try:
        loop.run_forever()
    finally:
        loop.close()
