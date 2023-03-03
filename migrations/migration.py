"""Migration sql scripts run."""
import logging
import os
import traceback
from datetime import datetime
from typing import Optional, NoReturn, List

from psycopg2 import connect
from psycopg2.errors import UndefinedTable


class Migration:
    """
    Run migration sql scripts.
    """

    file_log = logging.FileHandler('Log.migrations')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s]: %(message)s',
                        datefmt='%m.%d.%Y %H:%M:%S',
                        level=logging.INFO)

    def __init__(self, path: str, db: connect):
        """
        Init constructor.
        """
        self.path = path
        self.db = db

    def migrate(self, migrations: List) -> NoReturn:
        """Run migration scripts."""
        for migration in migrations:
            logging.info(f'Run migration: {migration}')

            with open(os.path.join(self.path, migration)) as migration_file:
                with self.db.cursor() as cursor:
                    try:
                        logging.info('Execute migration.')
                        cursor.execute(migration_file.read())

                        logging.info('Save migration in table migrations.')
                        cursor.execute("INSERT INTO migration (migration_name, created) VALUES (%s, %s);",
                                       (migration, datetime.now()))

                        logging.info('Commit.')
                        self.db.commit()
                    except:
                        traceback.print_exc()

        logging.info('Successfully exit.')

    def old_migrations(self) -> List:
        """
        Get completed migrations.
        """
        with self.db.cursor() as cursor:
            try:
                cursor.execute("SELECT migration_name FROM migration;")
            except UndefinedTable:
                cursor.execute('ROLLBACK')
                self.db.commit()
                return []

            return cursor.fetchall()

    def get_migrations(self, checking) -> Optional[List]:
        """
        Get new migrations.
        """
        if not checking:
            logging.info('Search new migrations...')

        new_migration = os.listdir(self.path)

        if not new_migration and not checking:
            logging.info('Migration folder sql is empty, exit.')

            return

        old_migrations = self.old_migrations()

        if not old_migrations and not checking:
            logging.info('Not old migration, start new migration.')
            new_migration.sort()

            return new_migration

        old_migrations = [m[0] for m in old_migrations]
        intersection_migrations = list(set(new_migration) - set(old_migrations))

        return intersection_migrations.sort()
