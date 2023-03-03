"""Module connection db."""
from psycopg2 import connect


class Database:
    """Connection db."""

    def __init__(self, conf):
        """
        Init settings.
        """
        self.conf = conf

    def connect(self):
        """
        Connection db.
        """
        conn = connect(
            user=self.conf['user'],
            port=self.conf['port'],
            database=self.conf['database'],
            password=self.conf['password'],
            host=self.conf['host'],
        )
        conn.set_session(isolation_level='SERIALIZABLE')

        return conn

    def __new__(cls, *args, **kwargs):
        """There is only one database connection."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)

        return cls.instance
