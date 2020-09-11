import os
from config import ConfigFromJSONFile


class Config7Z(ConfigFromJSONFile):

    def __init__(self):
        self.password = self._get_7z_password()
        self.exec = self._get_7z_exec()

    def _get_7z_password(self):
        return self.settings.get('7z_password')

    def _get_7z_exec(self):
        exe = self.settings.get('7z_exec')
        exe = 'c:\\Program Files\\7-Zip\\7z.exe' if exe is None else exe
        if isinstance(exe, str) and os.path.exists(exe):
            return exe
        raise Exception(f'Wrong path to 7z.exe file: {exe}')


conf_7z = Config7Z()
