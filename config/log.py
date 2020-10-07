import os
import logging
from config import ConfigFromJSONFile


class ConfigLog(ConfigFromJSONFile):
    def __init__(self):
        self.level = self._get_level()
        self.filename = self._get_filename()
        self.folder = self._get_folder()
        self.file = os.path.join(self.folder, self.filename)

    def _get_filename(self) -> str:
        filename = self.settings.get('log_filename')
        return filename or 'log.txt'

    def _get_folder(self) -> str:
        folder = self.settings.get('log_folder')
        return folder or os.getcwd()

    def _get_level(self) -> int:
        level = self.settings.get('log_level')
        if level is None or not isinstance(level, str) or level.lower() == 'info':
            return logging.INFO

        elif level.lower() == 'debug':
            return logging.DEBUG
        elif level.lower() == 'critical':
            return logging.CRITICAL
        elif level.lower() == 'error':
            return logging.ERROR
        elif level.lower() == 'warning':
            return logging.WARNING

        else:
            return logging.INFO


conf_log = ConfigLog()
