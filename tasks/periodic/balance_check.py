import asyncio
import time
import traceback
from datetime import datetime

from core.base_periodic_task import BasePeriodicTask


class BalanceCheck(BasePeriodicTask):
    """
    Periodic task for check balance
    """

    ROUTING_KEY = 'logger.event.send_message'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.send_message'

    async def prepare_message(self):
        if self.data and (datetime.utcnow() - datetime.fromtimestamp(self.data[-1]['ts'] / 1000)).seconds / 60 >= 3:
            message = f'BALANCES AND POSITION\n'

            total_position = 0
            total_balance = 0
            index_price = []
            no_need = []
            coin = self.data[0]['symbol'].split('USD')[0].replace('-', '').replace('/', '')
            for row in self.data:
                if coin in ['XBT', 'BTC']:
                    if not 'XBT' in row['symbol'] and 'BTC' not in row['symbol']:
                        continue
                else:
                    if not coin in row['symbol']:
                        continue
                if not row['exchange_name'] in no_need:
                    message += f"   EXCHANGE: {row['exchange_name']}\n"
                    message += f"ENV: {row['env']}\n"
                    message += f"TOT BAL: {row['total_balance']} USD\n"
                    message += f"POS: {round(row['pos'], 4)} {coin}\n"
                    message += f"AVL BUY:  {round(row['available_for_buy'])}\n"
                    message += f"AVL SELL: {round(row['available_for_sell'])}\n"
                    index_price.append((row['bid'] + row['ask']) / 2)
                    total_position += row['pos']
                    total_balance += row['total_balance']

                    no_need.append(row['exchange_name'])

            start_balance = await self.get_start_balance(no_need)

            message += f"   TOTAL:\n"
            message += f"START BALANCE: {round(start_balance, 2)} USD\n"
            message += f"CHANGE OF BALANCE ABS: {abs(start_balance - total_balance)}\n"
            message += f"TOTAL BALANCE: {round(total_balance, 2)} USD\n"
            message += f"POSITION: {round(total_position, 4)} {coin}\n"
            min_to_last_deal = round((time.time() - self.data[0]['ts']) / 60)
            message += f"LAST DEAL WAS {min_to_last_deal} MIN BEFORE\n"
            message += f"INDEX PX: {round(sum(index_price) / len(index_price), 2)} USD\n"

            self.data = {
                'chat_id': row['chat_id'],
                'bot_token': row['bot_token'],
                'msg': message
            }
            await self.__update_all()
            await self.send_to_rabbit()

    async def get_start_balance(self, no_need) -> float:
        names = '('
        for name in no_need:
            names += "'" + name + "'" + ","

        names = names[:-1] + ')'

        sql = f"""
            select 
                sum(d.total_balance) as bal
            from 
                (select 
                    distinct on (bc.exchange_name) bc.exchange_name, ts, total_balance
                from 
                    balance_check bc
                where 
                    bc.ts > extract(epoch from current_date at time zone 'UTC') * 1000 and 
                    bc.exchange_name in {names}
                order by 
                    exchange_name, ts
                ) d  
        """

        res = await self.cursor.fetchrow(sql)
        return res['bal']

    async def get_data(self) -> None:
        sql = """
            select 
                *
            from
               balance_check dc
            where 
                dc.was_sent = False
            order by
                dc.ts desc
            """
        self.data = await self.cursor.fetch(sql)

    async def __update_all(self):
        sql = """
            update 
                balance_check 
            set 
                was_sent = True
            where
                 was_sent = False
            """
        await self.cursor.execute(sql)


if __name__ == '__main__':
    worker = BalanceCheck()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run())
    except Exception as e:
        traceback.print_exc()
    finally:
        loop.close()
