from datetime import datetime, timedelta
from core.wrappers import try_exc_async


class DailyReport:

    def __init__(self):
        self.exchanges = ''
        self.pairs = ''
        self.start_balances = {}
        self.end_balances = {}

    @try_exc_async
    async def __get_active_exchanes(self):
        pass

    @try_exc_async
    async def __send_overall_summary(self):
        delimiter = '_______________________________________\n'
        total_start_balance = 0.0
        total_end_balance = 0.0

        message = f"DAILY REPORT FOR {datetime.today() - timedelta(days=1)}\n"
        message += f"ACTIVE EXCHANGES: {self.exchanges}\n"
        message += f"ACTIVE PAIRS: {self.pairs}\n"
        message += f"Theory profit: 5000\n"
        message += delimiter
        message += "START BALANCE, USD:\n"

        for exch, balance in self.start_balances.items():
            message += f"{exch.upper()}, USDT {balance}\n"
            total_start_balance += float(balance)

        message += "END BALANCE, USD:\n"

        for exch, balance in self.start_balances.items():
            message += f"{exch.upper()}, USDT {balance}\n"
            total_end_balance += float(balance)

        message += f"CHANGE OF BALANCE, USD: {total_end_balance - total_start_balance}\n"
        message += f"CHANGE OF BALANCE, %: {round(100 - total_end_balance * 100 / total_start_balance, 2)}\n"
        message += delimiter
        message += f'START DISBALANCE, USD: {1}'
