import logging
from logging.config import dictConfig

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class UpdateArbitragePossibilities:

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CHECK_ARBITRAGE_POSSIBILITIES'
        self.all_arbitrage_possibilities = []
        self.arbitrage_possibilities_to_update = []

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
           arbitrage_possibilities
        where 
            status = 'Processing' 
        """

        self.all_arbitrage_possibilities = [x['id'] for x in await cursor.fetch(sql)]

    async def __get_orders_by_parent_id(self, cursor):
        for parent_id in self.all_arbitrage_possibilities:
            sql = f"""
            select 
                status
            from
                orders
            where 
                parent_id = '{parent_id}'
            """

            data = await cursor.fetch(sql)




    async def __update_arbitrage_possibilities(self, cursor):
        for data in self.arbitrage_possibilities_to_update:
            sql = f"""
                    update 
                        arbitrage_possibilities
                    set 
                        status = '{data['status']}',
                        status_datetime = '{data['status_datetime']}',
                        status_ts = {data['ts_update']}
                    where 
                        id = '{data['id']}'
                    """
            await cursor.execute(sql)

    async def __publish_message(self):
        message = {

        }

        await publish_message()
