import logging
import time

from devtoolcm import TargetConfig
from devtoolcm import init_logging
from devtoolcm import target


def main():
    file_config: TargetConfig = target('core/file', {
        'path': 'test.txt',
        'content': f'Hello World: {time.time()}',
    })
    database_config: TargetConfig = target('postgresql/db', {
        'database_name': 'test_db',
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgres',
        'default_database': 'postgres'
    })


if __name__ == '__main__':
    init_logging(logging.INFO, include_logger_name=True)
    main()
