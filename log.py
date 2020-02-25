"""
    Модуль создания логов
"""

import shutil
import os
import logging

from settings import log as settings


def get_log():

    filename = os.path.join(
        settings['folder'],
        settings['filename']
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(filename)s[LINE:%(lineno)d]# %(levelname)s - %(message)s',
        filename=filename,
    )

    return logging.getLogger('buper')


def move_log(dst):

    log = get_log()

    try:
        if not os.path.exists(dst):
            os.mkdir(dst)

        dst_file = os.path.join(dst, settings['filename'])
        log.info(f'Перемещение лога в {dst_file}')

        logging.shutdown()
        shutil.move(settings['filename'], dst_file)

    except Exception as e:
        log.error(f'Не удалось переместить лог: {e}')


if __name__ == '__main__':
    pass
