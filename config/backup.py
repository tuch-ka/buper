import os
from config import ConfigFromJSONFile
from logger import log


class BackUpConfig(ConfigFromJSONFile):
    """
    Настройки резервной копии
    """
    def __init__(self):
        self.src = self._get_source()
        self.ignore = self._get_ignore()
        self.dst = self._get_destination()
        self.count = self._get_count()
        self.lifetime = self._get_lifetime()
        self.min_capacity = self._get_min_capacity()

    def _get_min_capacity(self, default: int = 3) -> int:
        min_capacity = self.settings.get('min_capacity')
        if isinstance(min_capacity, int):
            return min_capacity
        return default

    def _get_source(self, default: str = os.getcwd()) -> str:
        source = self.settings.get('source')
        if isinstance(source, str) and os.path.exists(source):
            return source
        return default

    def _get_ignore(self) -> list:
        ignore = self.settings.get('ignore')
        if ignore is not None \
                and isinstance(ignore, list) \
                and all([isinstance(folder, str) for folder in ignore]):
            return ignore
        return []

    def _get_destination(self, default: str = os.getcwd()) -> str:
        dst = self.settings.get('destination')
        if isinstance(dst, str):

            if os.path.exists(dst):
                return dst

            try:
                os.mkdir(dst)
                return dst
            except OSError:
                log.logger.error(f'Не удалось создать папку назначения: {dst}')
                log.logger.error(f'Будет использовано значение по умолчанию: {default}')

        return default

    def _get_count(self, default=0) -> int:
        count = self.settings.get('count')
        if not isinstance(count, int):
            try:
                count = int(count)
            except (ValueError, TypeError):
                count = default
        return count if count >= 0 else default

    def _get_lifetime(self, default=0) -> int:
        lifetime = self.settings.get('lifetime')
        if not isinstance(lifetime, int):
            try:
                lifetime = int(lifetime)
            except (ValueError, TypeError):
                lifetime = default
        return lifetime if lifetime >= 0 else default


conf_backup = BackUpConfig()
