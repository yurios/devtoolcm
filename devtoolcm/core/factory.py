from devtoolcm.core.types import TargetComparator
from devtoolcm.core.types import TargetConfig
from devtoolcm.core.types import TargetConfigurer
from devtoolcm.core.types import TargetCreator
from devtoolcm.core.types import TargetDeleter
from devtoolcm.core.types import TargetInstanceNamer
from devtoolcm.core.types import TargetReader
from devtoolcm.core.types import TargetUpdater

from devtoolcm.util import get_logger

log = get_logger()

__TARGET_CONFIGURER_REGISTRY = {}


def get_target_configurer(target_type: str) -> TargetConfigurer:
    target_configurer = __TARGET_CONFIGURER_REGISTRY.get(target_type)
    if not target_configurer:
        log.error(f"Unknown target type: {target_type}")
        exit(1)
    return target_configurer


def register_target_configurer(target_type: str, target_configurer: TargetConfigurer):
    if target_type in __TARGET_CONFIGURER_REGISTRY:
        log.error(f"Target type '{target_type}' already registered")
        exit(1)
    __TARGET_CONFIGURER_REGISTRY[target_type] = target_configurer


def create_target_configurer(
        target_type: str,
        instance_namer: TargetInstanceNamer,
        creator: TargetCreator,
        reader: TargetReader,
        updater: TargetUpdater,
        deleter: TargetDeleter,
        comparator: TargetComparator,
):
    log = get_logger(2)

    def target_configurer(target_config: TargetConfig) -> TargetConfig:
        target_instance_name = f"{target_type}({instance_namer(target_config)})"
        log.info(f"{target_instance_name}: Looking for a target...")
        existing_target_config = reader(target_config)
        if not existing_target_config:
            log.info(f"{target_instance_name}: Target does not exist. Creating...")
            existing_target_config = creator(target_config)
            log.info(f"{target_instance_name}: Target created")
            return existing_target_config
        difference = comparator(target_config, existing_target_config)
        if difference:
            log.info(f"{target_instance_name}: Existing target does not match expected state:")
            for diff in difference:
                log.info(f"{target_instance_name}: - {diff}")
            log.info(f"{target_instance_name}: Updating existing target...")
            existing_target_config = updater(target_config)
            log.info(f"{target_instance_name}: Target updated")
            return existing_target_config
        log.info(f"{target_instance_name}: Target is in the expected state")
        return existing_target_config

    register_target_configurer(target_type, target_configurer)
