import asyncio
import orjson

import aiohttp

from config import Config


class Telegram:

    def __init__(self, app):
        self.telegram_api_url = f'https://api.telegram.org/bot1965694823:AAEgOeKyXjTATWDbBbRGpivqh5i2IR6FzjY/sendMessage'
        self.headers = {'Content-Type': 'application/json'}

    async def run(self, payload: dict) -> None:
        message = {
            'chat_id': payload['chat_id'],
            'text': '<pre>' + payload['msg'] + '</pre>',
            'parse_mode': 'HTML'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.telegram_api_url, data=orjson.dumps(message), headers=self.headers) as resp:
                if resp.status != 200:
                    await asyncio.sleep(10)
                    await self.run(payload)


if __name__ == '__main__':
    worker = Telegram({})
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run({}))
    except Exception as e:
        print(e)
    finally:
        loop.close()