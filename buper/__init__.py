import sys

from .linux import LinuxBuper
from .windows import WindowsBuper

from logger import logger


class Buper:

    def __new__(cls, *args, **kwargs):
        if sys.platform == 'win32':
            logger.debug(f'ОС: {sys.platform}')
            return WindowsBuper()

        elif sys.platform in ('linux', 'linux2'):
            logger.debug(f'ОС: {sys.platform}')
            return LinuxBuper()

        else:
            logger.error(f'Определена не поддерживаемая ОС: {sys.platform}')
            raise NotImplemented
