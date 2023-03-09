import asyncio
import traceback

from tasks.periodic.balance_check import BalanceCheck
from tasks.periodic.balancing_reports import BalancingReports
from tasks.periodic.deals_reports import DealsReports

TASKS = [
    BalanceCheck(),
    # BalancingReports(),
    DealsReports()
]


async def run() -> None:
    """
    Just task runner
    :return:
    """
    while True:
        for task in TASKS:
            await task.run()
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run())
    except Exception as e:
        traceback.print_exc()
    finally:
        loop.close()
