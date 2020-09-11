from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL, SMTPException

from config.mail import conf_email
from logger import log, logger


class Mail:

    def __init__(self, text: str):
        self.text = text
        self.message = self._generate_message()

    def send(self):

        if not conf_email.mail_enable:
            logger.info('Отправка email отключена')
            return None

        mail_server = SMTP_SSL(
            conf_email.server,
            conf_email.port,
        )

        try:
            mail_server.login(
                conf_email.user,
                conf_email.password,
            )

            mail_server.send_message(
                self.message
            )

            logger.info('Email успешно отправлен на сервер')

        except SMTPException as e:
            logger.error(f'Ошибка при отправке email: {e}')

        finally:
            mail_server.quit()

    def _generate_message(self):

        message = MIMEMultipart()

        message['Subject'] = f'BackUp {(datetime.now()).strftime("%Y-%m-%d")}'
        message['From'] = conf_email.user
        message['To'] = conf_email.to_address

        message.attach(MIMEText(self.text, 'plain', 'utf-8'))

        file = MIMEText(log.read_log())
        file.add_header('Content-Disposition', 'attachment', filename='log.txt')
        message.attach(file)

        return message

