import argparse
import os

from config import Config
from migrations.database import Database
from migrations.migration import Migration


def main(checking):
    """ Migration run. """
    path = os.path.join('/migrations', 'versions')
    db = Database(conf=Config.POSTGRES).connect()

    migration = Migration(path=path, db=db)
    migrations = migration.get_migrations(checking=checking)

    if not checking:
        migration.migrate(migrations=migrations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args()

    main(checking=args.c)
