import json
import os


class Config:
    settings = json.load(open('settings.json', 'r'))

    def __init__(self):
        # Настройки резервных копий
        self.src = self._get_source()
        self.ignore = self._get_ignore()
        self.dst = self._get_destination()
        self.count = self._get_count()
        self.lifetime = self._get_lifetime()

        # Настройки архиватора
        self.password_7z = self._get_7z_password()
        self.exec_7z = self._get_7z_exec()

        # Настройки почты
        self.mail_enable = self._get_mail_enable()
        self.server = self._get_server()
        self.port = self._get_port()
        self.to_address = self._get_to_address()
        self.user = self._get_user()
        self.password = self._get_password()

    def _get_source(self) -> str:
        source = self.settings.get('source')
        if isinstance(source, str) and os.path.exists(source):
            return source
        return os.getcwd()

    def _get_ignore(self) -> list:
        ignore = self.settings.get('ignore')
        if ignore is not None and isinstance(ignore, list) and all([isinstance(i, str) for i in ignore]):
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
            except Exception:
                pass

        return os.getcwd()

    def _get_count(self) -> int:
        count = self.settings.get('count')
        if isinstance(count, int) and count >= 0:
            return count
        return 0

    def _get_lifetime(self) -> int:
        lt = self.settings.get('lifetime')
        if isinstance(lt, int) and lt >= 0:
            return lt
        return 0

    def _get_7z_password(self) -> str:
        password = self.settings.get('7z_password')
        if isinstance(password, str):
            return password
        return ''

    def _get_7z_exec(self):
        exe = self.settings.get('7z_exec')
        if isinstance(exe, str) and os.path.exists(exe):
            return exe
        raise Exception(f'Wrong path to 7z.exe file: {exe}')

    def _get_mail_enable(self) -> bool:
        mail_enable = self.settings.get('mail_enable')
        if isinstance(mail_enable, bool):
            return mail_enable
        return False

    def _get_server(self):
        return self.settings.get('server')

    def _get_port(self) -> int:
        port = self.settings.get('port')
        if isinstance(port, int):
            return port
        return 25

    def _get_to_address(self):
        return self.settings.get('to_address')

    def _get_user(self):
        return self.settings.get('user')

    def _get_password(self):
        return self.settings.get('password')


config = Config()
