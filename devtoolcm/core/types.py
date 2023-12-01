from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

# type definitions
TargetConfig = Dict[str, 'Config']
TargetInstanceNamer = Callable[[TargetConfig], str]
TargetCreator = Callable[[TargetConfig], TargetConfig]
TargetReader = Callable[[TargetConfig], Optional[TargetConfig]]
TargetUpdater = Callable[[TargetConfig], TargetConfig]
TargetDeleter = Callable[[TargetConfig], None]
TargetComparator = Callable[[TargetConfig, TargetConfig], List[str]]
TargetConfigurer = Callable[[TargetConfig], TargetConfig]
