import os
from typing import Optional, List

from devtoolcm.core.factory import create_target_configurer
from devtoolcm.core.types import TargetConfig
from devtoolcm.util import get_logger

log = get_logger()


def name(expected_target: TargetConfig) -> str:
    return expected_target['path']


def create(expected_target: TargetConfig) -> TargetConfig:
    try:
        with open(expected_target['path'], "w") as file:
            file.write(expected_target['content'])
        return expected_target
    except Exception as e:
        log.error(f"Error creating the file: {e}")
        exit(1)


def read(expected_target: TargetConfig) -> Optional[TargetConfig]:
    try:
        with open(expected_target['path'], "r") as file:
            content = file.read()
        return {
            'path': expected_target['path'],
            'content': content
        }
    except FileNotFoundError:
        return None
    except Exception as e:
        log.error(f"Error reading the file: {e}")
        exit(1)


def update(expected_target: TargetConfig, existing_target: TargetConfig) -> TargetConfig:
    if expected_target['path'] != existing_target['path']:
        delete(existing_target)
        create(expected_target)
    if expected_target['content'] != existing_target['content']:
        try:
            with open(expected_target['path'], "w") as file:
                file.write(expected_target['content'])
            return expected_target
        except Exception as e:
            log.error(f"Error replacing the file content: {e}")
            exit(1)


def delete(existing_target: TargetConfig) -> None:
    try:
        os.remove(existing_target['path'])
        return None
    except FileNotFoundError:
        pass
    except Exception as e:
        log.error(f"Error deleting the file: {e}")
        exit(1)


def compare(expected_target: TargetConfig, existing_target: TargetConfig) -> List[str]:
    difference = []
    if expected_target['path'] != existing_target['path']:
        difference.append(f"Path should be {expected_target['path']}")
    if expected_target['content'] != existing_target['content']:
        difference.append(f"Content should be {expected_target['content']}")
    return difference


create_target_configurer(
    target_type='core/file',
    name=name,
    create=create,
    read=read,
    update=update,
    delete=delete,
    compare=compare,
)
