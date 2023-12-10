from migrations.database import Database
from migrations.migration import Migration
import configparser
from core.wrappers import try_exc_regular

config = configparser.ConfigParser()
config.read('config.ini', "utf-8")


@try_exc_regular
def main(checking=True):
    """ Migration run. """
    path = '/home/ubuntu/logger/migrations/versions'
    db = Database(conf={'database': config['POSTGRES']['NAME'],
                        'user': config['POSTGRES']['USER'],
                        'password': config['POSTGRES']['PASSWORD'],
                        'host': config['POSTGRES']['HOST'],
                        'port': config['POSTGRES']['PORT'],
                        }).connect()
    print('DB CONNECTED')
    migration = Migration(path=path, db=db)
    migrations = migration.get_migrations(checking=checking)

    if not checking:
        migration.migrate(migrations=migrations)


if __name__ == '__main__':
    main()
