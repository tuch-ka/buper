"""
    Модуль отправки электронных писем
"""

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

from settings import mail
from log import get_log, get_log_content


def generate_message(msg):

    message = MIMEMultipart()

    message['Subject'] = f'BackUp {(datetime.now()).strftime("%Y-%m-%d")}'
    message['From'] = mail['from']
    message['To'] = mail['to']

    message.attach(MIMEText(f'Размер архива: {msg}', 'plain', 'utf-8'))

    file = MIMEText(get_log_content())
    file.add_header('Content-Disposition', 'attachment', filename='log.txt')
    message.attach(file)

    return message


def send_mail(msg):

    log = get_log()

    mail_server = SMTP(
        mail['server'],
        mail['port']
    )
    mail_server.starttls()

    try:
        mail_server.login(
            mail['from'],
            mail['password']
        )

        mail_server.send_message(
            generate_message(msg)
        )

        log.info('Email успешно отправлен на сервер')

    except Exception as e:
        log.error(f'Ошибка при отправке email: {e}')

    finally:
        mail_server.quit()


if __name__ == '__main__':
    send_mail()
