from config import ConfigFromJSONFile


class EMailConfig(ConfigFromJSONFile):
    """
    Настройки почтового сервера
    """
    def __init__(self):
        self.mail_enable = self._get_mail_enable()
        self.server = self._get_server()
        self.port = self._get_port()
        self.to_address = self._get_to_address()
        self.user = self._get_user()
        self.password = self._get_password()

    def _get_mail_enable(self) -> bool:
        mail_enable = self.settings.get('mail_enable')
        if isinstance(mail_enable, bool):
            return mail_enable
        return False

    def _get_server(self):
        return self.settings.get('server')

    def _get_port(self, default=465) -> int:
        port = self.settings.get('port')
        if not isinstance(port, int):
            try:
                port = int(port)
            except (ValueError, TypeError):
                port = default
        return port

    def _get_to_address(self):
        return self.settings.get('to_address')

    def _get_user(self):
        return self.settings.get('user')

    def _get_password(self):
        return self.settings.get('password')


conf_email = EMailConfig()
