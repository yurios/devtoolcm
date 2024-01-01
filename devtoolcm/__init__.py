# import target handlers to self-register them
import devtoolcm.target

# other imports
from devtoolcm.core.factory import get_target_configurer
from devtoolcm.core.types import TargetConfig
from devtoolcm.core.types import TargetConfigurer
from devtoolcm.util import get_logger
from devtoolcm.util import init_logging


def target(target_type: str, target_config: TargetConfig) -> TargetConfig:
    target_configurer: TargetConfigurer = get_target_configurer(target_type)
    return target_configurer(target_config)
