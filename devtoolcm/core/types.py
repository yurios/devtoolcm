from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

# type definitions
TargetConfig = Dict[str, 'Config']
TargetName = Callable[[TargetConfig], str]
TargetCreate = Callable[[TargetConfig], TargetConfig]
TargetRead = Callable[[TargetConfig], Optional[TargetConfig]]
TargetUpdate = Callable[[TargetConfig, TargetConfig], TargetConfig]
TargetDelete = Callable[[TargetConfig], None]
TargetCompare = Callable[[TargetConfig, TargetConfig], List[str]]
TargetConfigurer = Callable[[TargetConfig], TargetConfig]
