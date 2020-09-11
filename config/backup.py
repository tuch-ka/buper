import os
from config import ConfigFromJSONFile


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

    def _get_source(self) -> str:
        source = self.settings.get('source')
        if isinstance(source, str) and os.path.exists(source):
            return source
        return os.getcwd()

    def _get_ignore(self) -> list:
        ignore = self.settings.get('ignore')
        if ignore is not None \
                and isinstance(ignore, list) \
                and all([isinstance(folder, str) for folder in ignore]):
            return ignore
        return []

    def _get_destination(self) -> str:
        dst = self.settings.get('destination')
        if isinstance(dst, str):

            if os.path.exists(dst):
                return dst

            try:
                os.mkdir(dst)
                return dst
            except OSError:
                pass

        return os.getcwd()

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
