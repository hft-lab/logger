import asyncio

from tasks.periodic.BalanceCheck import BalanceCheck
from tasks.periodic.BalancingReports import BalancingReports
from tasks.periodic.DealsReports import DealsReports

TASKS = [
    BalanceCheck(),
    BalancingReports(),
    DealsReports()
]


async def run() -> None:
    """
    Just task runner
    :return:
    """
    for task in TASKS:
        await task.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run())
    except Exception as e:
        print(e)
    finally:
        loop.close()
