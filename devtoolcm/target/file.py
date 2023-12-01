import os
from typing import Optional, List

from devtoolcm.core.factory import create_target_configurer
from devtoolcm.core.types import TargetConfig
from devtoolcm.util import get_logger

log = get_logger()


def namer(target_config: TargetConfig) -> str:
    return target_config['path']


def creator(target_config: TargetConfig) -> TargetConfig:
    try:
        with open(target_config['path'], "w") as file:
            file.write(target_config['content'])
        return target_config
    except Exception as e:
        log.error(f"Error creating the file: {e}")
        exit(1)


def reader(target_config: TargetConfig) -> Optional[TargetConfig]:
    try:
        with open(target_config['path'], "r") as file:
            content = file.read()
        return {
            'path': target_config['path'],
            'content': content
        }
    except FileNotFoundError:
        return None
    except Exception as e:
        log.error(f"Error reading the file: {e}")
        exit(1)


def updater(target_config: TargetConfig) -> TargetConfig:
    try:
        with open(target_config['path'], "w") as file:
            file.write(target_config['content'])
        return target_config
    except Exception as e:
        log.error(f"Error replacing the file content: {e}")
        exit(1)


def deleter(target_config: TargetConfig) -> None:
    try:
        os.remove(target_config['path'])
        return None
    except FileNotFoundError:
        pass
    except Exception as e:
        log.error(f"Error deleting the file: {e}")
        exit(1)


def comparator(expected: TargetConfig, existing: TargetConfig) -> List[str]:
    difference = []
    if expected['path'] != existing['path']:
        difference.append(f"Path should be {expected['path']}")
    if expected['content'] != existing['content']:
        difference.append(f"Content should be {expected['content']}")
    return difference


file_configurer = create_target_configurer(
    target_type='core/file',
    instance_namer=namer,
    creator=creator,
    reader=reader,
    updater=updater,
    deleter=deleter,
    comparator=comparator,
)
