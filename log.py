"""
    Модуль создания логов
"""

import shutil
import os
import logging

from settings import log as settings

log_file = os.path.join(
        settings['folder'],
        settings['filename']
    )


def get_log_content():
    if not os.path.exists(log_file):
        return ''
    with open(log_file, 'r') as file:
        text = file.read()
    return text


def get_log():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(filename)s[LINE:%(lineno)d]# %(levelname)s - %(message)s',
        filename=log_file,
    )

    return logging.getLogger('buper')


def move_logs(dst_folder):

    log = get_log()

    try:
        if not os.path.exists(dst_folder):
            os.mkdir(dst_folder)

        dst_file = os.path.join(dst_folder, settings['filename'])

        logging.shutdown()
        shutil.move(log_file, dst_file)

    except Exception as e:
        log.error(f'Не удалось переместить лог: {e}')


if __name__ == '__main__':
    pass
