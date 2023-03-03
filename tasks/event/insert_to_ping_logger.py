import logging
from datetime import datetime
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToPingLogging:
    """
    Class for insert to ping_logging table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'INSERT_TO_PING_LOGGING'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload: dict with NOT NULL params (
            1. Server Name (Location)
            2. Exchange Name
            3. Status of ping to Exch. (Enum: success, no_connection)
            4. Timestamp of request (ms)
            5. Timestamp from response (ms)
            6. Timestamp of the received response on our side (ms))
        :return: None
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_ping_logger(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_ping_logger(data: dict, cursor) -> None:
        """
        Insert data to ping_logger table
        :param data: dict with NOT NULL keys: server_name, exchange_name, status_of_ping,
                                              ts_of_request, ts_from_response, ts_received_response
        :param cursor: asyncpg cursor
        :return: None
        """
        sql = f"""
            insert into ping_logging(
                server_name, 
                exchange_name, 
                status_of_ping, 
                ts_of_request, 
                ts_from_response, 
                ts_received_response)
            values(
                '{data["server_name"]}', 
                '{data["exchange_name"]}', 
                '{data["status_of_ping"]}', 
                {data["ts_of_request"]}, 
                {data["ts_from_response"]}, 
                {data["ts_received_response"]})         
            """
        await cursor.execute(sql)
