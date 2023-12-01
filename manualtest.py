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
    print(file_config)


if __name__ == '__main__':
    init_logging(logging.INFO, include_logger_name=True)
    main()
