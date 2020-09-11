import os
from config import ConfigFromJSONFile


class Config7Z(ConfigFromJSONFile):

    def __init__(self):
        self.password_7z = self._get_7z_password()
        self.exec_7z = self._get_7z_exec()

    def _get_7z_password(self):
        return self.settings.get('7z_password')

    def _get_7z_exec(self):
        exe = self.settings.get('7z_exec')
        # TODO: для отладки в ubuntu
        return exe
        # if isinstance(exe, str) and os.path.exists(exe):
        #     return exe
        # raise Exception(f'Wrong path to 7z.exe file: {exe}')


conf_7z = Config7Z()
