import asyncio
import orjson
from core.wrappers import try_exc_async

import aiohttp

import configparser
config = configparser.ConfigParser()
config.read('config.ini', "utf-8")


class Telegram:

    def __init__(self, app):
        self.telegram_api_url = 'https://api.telegram.org/bot{}/sendMessage'
        self.headers = {'Content-Type': 'application/json'}

    @try_exc_async
    async def run(self, payload: dict) -> None:
        message = {
            'chat_id': payload['chat_id'],
            'text': '<pre>' + str(payload['msg']) + '</pre>',
            'parse_mode': 'HTML'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.telegram_api_url.format(payload['bot_token']), data=orjson.dumps(message),
                                    headers=self.headers) as resp:
                if resp.status != 200:
                    pass
                    # Создать модуль логирования в файл
                    # await asyncio.sleep(10)
                    # await self.run(payload)


if __name__ == '__main__':
    pass









