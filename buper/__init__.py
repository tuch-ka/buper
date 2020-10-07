import sys
from .linux import LinuxBuper
from .windows import WindowsBuper


class Buper:

    def __new__(cls, *args, **kwargs):
        if sys.platform == 'win32':
            return WindowsBuper()

        elif sys.platform in ('linux', 'linux2'):
            return LinuxBuper()

        else:
            raise NotImplemented
