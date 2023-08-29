import asyncio
import orjson

import aiohttp

import configparser
import sys
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")


class Telegram:

    def __init__(self, app):
        self.telegram_api_url = 'https://api.telegram.org/bot{}/sendMessage'
        self.headers = {'Content-Type': 'application/json'}

    async def run(self, payload: dict) -> None:
        message = {
            'chat_id': payload['chat_id'],
            'text': '<pre>' + payload['msg'] + '</pre>',
            'parse_mode': 'HTML'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.telegram_api_url.format(payload['bot_token']), data=orjson.dumps(message),
                                    headers=self.headers) as resp:
                if resp.status != 200:
                    await asyncio.sleep(10)
                    await self.run(payload)


if __name__ == '__main__':
    from aio_pika import connect_robust
    from aiohttp.web import Application

    async def connect_to_rabbit():
        app['mq'] = await connect_robust(rabbit_url, loop=loop)


    rabbit = config['RABBIT']
    rabbit_url = f"amqp://{rabbit['USERNAME']}:{rabbit['PASSWORD']}@{rabbit['HOST']}:{rabbit['PORT']}/"
    app = Application()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_to_rabbit())
    worker = Telegram(app)
    loop.run_until_complete(worker.run({'bot_token': '6037890725:AAHSKzK9aazvOYU2AiBSDO8ZLE5bJaBNrBw',
                                        'chat_id': -807300930,
                                        'msg': 'TEST'}))









