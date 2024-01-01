from typing import List, Optional

from devtoolcm.core.factory import create_target_configurer
from devtoolcm.core.types import TargetConfig
from devtoolcm.target.postgresql.core import open_connection
from devtoolcm.util import get_logger

log = get_logger()


def name(expected_target: TargetConfig) -> str:
    return expected_target['database_name']


def create(expected_target: TargetConfig) -> TargetConfig:
    try:
        database_name = expected_target['database_name']
        with open_connection(expected_target) as connection:
            connection.autocommit = True
            connection.execute('create database ' + database_name)
        return expected_target
    except Exception as e:
        log.error(f"Error creating the database: {e}")
        exit(1)


def read(expected_target: TargetConfig) -> Optional[TargetConfig]:
    with open_connection(expected_target) as connection:
        query = ('select datname '
                 'from pg_database '
                 'where'
                 ' not datistemplate'
                 ' and datname = %(datname)s')
        cursor = connection.execute(query, {'datname': expected_target['database_name']})
        row = cursor.fetchone()
        if not row:
            return None
        return expected_target


def update(expected_target: TargetConfig, existing_target: TargetConfig) -> TargetConfig:
    return existing_target


def delete(existing_target: TargetConfig) -> None:
    connection = open_connection(existing_target)
    connection.execute('drop database ' + existing_target['database_name'])
    return None


def compare(expected_target: TargetConfig, existing_target: TargetConfig) -> List[str]:
    difference = []
    if expected_target['database_name'] != existing_target['database_name']:
        difference.append(f"Database name should be {expected_target['database_name']}")
    return difference


create_target_configurer(
    target_type='postgresql/db',
    name=name,
    create=create,
    read=read,
    update=update,
    delete=delete,
    compare=compare,
)
