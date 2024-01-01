from devtoolcm.core.types import TargetConfig
from pgdb import Connection, connect


def open_connection(target_config: TargetConfig) -> Connection:
    return connect(
        host=target_config['host'],
        port=target_config['port'],
        user=target_config['user'],
        password=target_config['password'],
        database=target_config['default_database'],
    )
