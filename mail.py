"""
    Модуль отправки электронных писем
"""

from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP

from settings import mail
from log import get_mail_log, get_log_content


def generate_message():

    message = MIMEText(get_log_content(), 'plain', 'utf-8')

    message['Subject'] = f'BackUp system {(datetime.now()).strftime("%Y-%m-%d")}'
    message['From'] = mail['from']
    message['To'] = mail['to']

    return message


def send_mail():

    log = get_mail_log()

    mail_server = SMTP(
        mail['server'],
        mail['port']
    )

    try:
        mail_server.login(
            mail['from'],
            mail['password']
        )

        mail_server.sendmail(
            mail['from'],
            mail['to'],
            generate_message().as_string()
        )

        log.info('Email успешно отправлен на сервер')

    except Exception as e:
        log.error(f'Ошибка при отправке email: {e}')

    finally:
        mail_server.quit()


if __name__ == '__main__':
    send_mail()
