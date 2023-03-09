import asyncio

from core.base_periodic_task import BasePeriodicTask


class BalancingReports(BasePeriodicTask):
    """
    Periodic task for balancing reports
    """

    ROUTING_KEY = 'logger.event.send_message'
    EXCHANGE_NAME = 'logger.event'
    QUEUE_NAME = 'logger.event.send_message'
    CHAT_ID = -853372015

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
