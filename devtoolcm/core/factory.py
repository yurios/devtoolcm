from devtoolcm.core.types import TargetCompare
from devtoolcm.core.types import TargetConfig
from devtoolcm.core.types import TargetConfigurer
from devtoolcm.core.types import TargetCreate
from devtoolcm.core.types import TargetDelete
from devtoolcm.core.types import TargetName
from devtoolcm.core.types import TargetRead
from devtoolcm.core.types import TargetUpdate

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
        name: TargetName,
        create: TargetCreate,
        read: TargetRead,
        update: TargetUpdate,
        delete: TargetDelete,
        compare: TargetCompare,
):
    log = get_logger(2)

    def target_configurer(expected_target: TargetConfig) -> TargetConfig:
        target_name = f"{target_type}[{name(expected_target)}]"
        log.info(f"{target_name}: Looking for a target...")
        existing_target = read(expected_target)
        if not existing_target:
            log.info(f"{target_name}: Target does not exist. Creating...")
            existing_target = create(expected_target)
            log.info(f"{target_name}: Target created")
            return existing_target
        difference = compare(expected_target, existing_target)
        if difference:
            log.info(f"{target_name}: Existing target does not match expected state:")
            for diff in difference:
                log.info(f"{target_name}: - {diff}")
            log.info(f"{target_name}: Updating existing target...")
            existing_target = update(expected_target, existing_target)
            log.info(f"{target_name}: Target updated")
            return existing_target
        log.info(f"{target_name}: Target is in the expected state")
        return existing_target

    register_target_configurer(target_type, target_configurer)
