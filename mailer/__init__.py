from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL, SMTPException

from config.mail import conf_email
from logger import logger


class Mail:

    def __init__(self, content: str, attachment: str = None, attachment_name: str = 'log.txt'):
        self.content = content
        self.attachment = attachment
        self.attachment_name = attachment_name
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
        """Генерирует объект сообщения"""
        message = MIMEMultipart()

        message['Subject'] = f'BackUp {(datetime.now()).strftime("%Y-%m-%d")}'
        message['From'] = conf_email.user
        message['To'] = conf_email.to_address

        message.attach(MIMEText(self.content, 'plain', 'utf-8'))

        if self.attachment is not None and isinstance(self.attachment_name, str):
            attachment = MIMEText(self.attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=self.attachment_name)
            message.attach(attachment)

        return message

