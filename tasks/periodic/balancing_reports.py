import asyncio

from core.base_periodic_task import BasePeriodicTask


class BalancingReports(BasePeriodicTask):
    """
    Periodic task for balancing reports
    """

    EXCHANGE_NAME = 'logger.event.telegram'
    ROUTING_KEY = 'logger.event'
    QUEUE_NAME = 'logger.event.telegram'

    async def prepare_message(self):
        pass

    async def get_data(self):
        pass


if __name__ == '__main__':
    worker = BalancingReports()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(worker.run())
    except Exception as e:
        print(e)
    finally:
        loop.close()
