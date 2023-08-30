from migrations.database import Database
from migrations.migration import Migration
import configparser
import sys
import os
config = configparser.ConfigParser()
config.read(sys.argv[1], "utf-8")


def main(checking=True):
    """ Migration run. """
    path = os.path.join('/migrations', 'versions')
    db = Database(conf={'database': config['POSTGRES']['NAME'],
                        'user': config['POSTGRES']['USER'],
                        'password': config['POSTGRES']['PASSWORD'],
                        'host': config['POSTGRES']['HOST'],
                        'port': config['POSTGRES']['PORT'],
                        }).connect()

    migration = Migration(path=path, db=db)
    migrations = migration.get_migrations(checking=checking)

    if not checking:
        migration.migrate(migrations=migrations)


if __name__ == '__main__':
    main()
