import logging
import os
import shutil

from config.log import conf_log


class Log:

    @staticmethod
    def get_logger():
        """
        Возвращает объект logger
        """
        logging.basicConfig(
            level=conf_log.level,
            format='%(asctime)s: %(filename)s[LINE:%(lineno)d]# %(levelname)s - %(message)s',
            filename=conf_log.file,
        )

        return logging.getLogger('buper')

    @staticmethod
    def read_log() -> str:
        """
        Считывает информацию из лог-файла
        """
        try:
            with open(conf_log.filename, 'r') as file:
                message = file.read()

        except FileNotFoundError:
            message = f'Не найден файл: {conf_log.filename}'

        except Exception as error:
            message = f'Произошла непредвиденная ошибка: {error}'

        return message

    def move(self, dst) -> None:
        """
        Перемещает лог-файл в указанную папку
        """
        if not os.path.exists(dst):
            try:
                os.mkdir(dst)
            except OSError as error:
                log = self.get_logger()
                log.error(f'Не удалось переместить лог.\nОшибка при создании папки "{dst}":\n{error}')
                return None

        dst_file = os.path.join(dst, conf_log.filename)
        logging.shutdown()

        try:
            shutil.move(conf_log.file, dst_file)
        except shutil.Error as error:
            log = self.get_logger()
            log.error(f'Не удалось переместить лог.\nОшибка при перемещении в {dst_file}:\n{error}')

        return None
