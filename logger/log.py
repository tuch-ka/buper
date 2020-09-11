import logging
import os
import shutil

from config.log import conf_log


class Log:

    @staticmethod
    def get_log():
        """
        Возвращает объект logger
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s: %(filename)s[LINE:%(lineno)d]# %(levelname)s - %(message)s',
            filename=conf_log.filename,
        )

        return logging.getLogger('buper')

    @staticmethod
    def read_log() -> str:
        """
        Считывает информацию из лог-файла
        """
        if not os.path.exists(conf_log.filename):
            return ''

        with open(conf_log.filename, 'r') as file:
            message = file.read()
        return message

    @classmethod
    def move(cls, dst) -> None:
        """
        Перемещает лог-файл в указанную папку
        """
        if not os.path.exists(dst):
            try:
                os.mkdir(dst)
            except OSError as error:
                log = cls.get_log()
                log.error(f'Не удалось переместить лог.\nОшибка при создании папки "{dst}":\n{error}')
                return None

        dst_file = os.path.join(dst, conf_log.filename)
        logging.shutdown()

        try:
            shutil.move(conf_log.file, dst_file)
        except shutil.Error as error:
            log = cls.get_log()
            log.error(f'Не удалось переместить лог.\nОшибка при перемещении в {dst_file}:\n{error}')

        return None
