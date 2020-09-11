import os
from config import ConfigFromJSONFile


class ConfigLog(ConfigFromJSONFile):
    def __init__(self):
        self.filename = self._get_filename()
        self.folder = self._get_folder()
        self.file = os.path.join(self.folder, self.filename)

    def _get_filename(self):
        filename = self.settings.get('log_filename')
        return filename if filename is not None else 'log.txt'

    def _get_folder(self):
        folder = self.settings.get('log_folder')
        return folder if folder is not None else os.getcwd()


conf_log = ConfigLog()
