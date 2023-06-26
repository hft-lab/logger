import datetime
import logging
import time
from logging.config import dictConfig

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)



class OrderStatuses:
    SUCCESS = 'Fully Executed'
    UNSUCCESS = 'Not Executed'

class DisbalanceStatuses:
    SUCCESS = 'Success'
    UNSUCCESS = 'Unsuccess'
    PARTIAL_SUCCESS = 'Partial_success'


class CheckAndUpdateDisbalances:
    ROUTING_KEY = 'logger.event.check_balance'
    EXCHANGE_NAME = 'logger.event.'
    QUEUE_NAME = 'logger.event.check_balance'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CHECK_AND_UPDATE_DISBALANCES'
        self.all_disbalances = []
        self.disbalances_to_update = []

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")

        async with self.app['db'].acquire() as cursor:
            await self.__get_all_processing_arbitrage_possibilities_ids(cursor)
            await self.__get_orders_by_parent_id(cursor)
            await self.__update_arbitrage_possibilities(cursor)

        logger.info(f"Finish: {self.worker_name}")

    async def __get_all_processing_arbitrage_possibilities_ids(self, cursor):
        sql = """
        select 
            id
        from 
           disbalances
        where 
            status = 'Processing' 
        order by
            ts desc
        """

        self.all_disbalances = [x['id'] for x in await cursor.fetch(sql)]

    async def __get_orders_by_parent_id(self, cursor):
        for parent_id in self.all_disbalances:
            sql = f"""
            select 
                status
            from
                orders
            where 
                parent_id = '{parent_id}'
            """

            data = await cursor.fetch(sql)
            in_processing = False
            else_statuses = []

            for row in data:
                if row['status'] == 'Processing':
                    in_processing = True
                elif row['status'] == OrderStatuses.SUCCESS:
                    else_statuses.append(True)
                elif row['status'] == OrderStatuses.UNSUCCESS:
                    else_statuses.append(False)

            if not in_processing and all(else_statuses):
                self.disbalances_to_update.append(
                    {
                        'id': parent_id,
                        'status': DisbalanceStatuses.SUCCESS,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time()
                    }
                )
            elif not in_processing and any(else_statuses):
                self.disbalances_to_update.append(
                    {
                        'id': parent_id,
                        'status': DisbalanceStatuses.PARTIAL_SUCCESS,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time()
                    }
                )
            elif not in_processing and not all(else_statuses):
                self.disbalances_to_update.append(
                    {
                        'id': parent_id,
                        'status': DisbalanceStatuses.UNSUCCESS,
                        'status_datetime': datetime.datetime.utcnow(),
                        'status_ts': time.time()
                    }
                )

    async def __update_arbitrage_possibilities(self, cursor):
        for data in self.disbalances_to_update:
            sql = f"""
                    update 
                        disbalances
                    set 
                        status = '{data['status']}',
                        status_datetime = '{data['status_datetime']}',
                        status_ts = {data['status_ts']}
                    where 
                        id = '{data['id']}'
                    """

            await cursor.execute(sql)
            await self.__publish_message(data['id'])

    async def __publish_message(self, id):
        message = {
            'parent_id': str(id),
            'context': 'post-balancing',
            'env': 'TOKYO_DEV',
            'chat_id': -807300930,
            'telegram_bot': '6037890725:AAHSKzK9aazvOYU2AiBSDO8ZLE5bJaBNrBw'
        }

        await publish_message(
            connection=self.app['mq'],
            message=message,
            exchange_name=self.EXCHANGE_NAME,
            routing_key=self.ROUTING_KEY,
            queue_name=self.QUEUE_NAME
        )
