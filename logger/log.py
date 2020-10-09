import logging
import os
import shutil

from config.log import conf_log


class Log:

    def __init__(self):
        self.level = conf_log.level
        self.filename = conf_log.filename
        self.folder = conf_log.folder
        self.file = os.path.join(self.folder, self.filename)

        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = self.get_logger()
        return self._logger

    def get_logger(self):
        """
        Возвращает объект logger
        """
        logging.basicConfig(
            level=self.level,
            format='%(asctime)s: %(filename)s[LINE:%(lineno)d]# %(levelname)s - %(message)s',
            filename=self.file,
        )

        return logging.getLogger('buper')

    def read_log(self) -> str:
        """
        Считывает информацию из лог-файла
        """
        try:
            with open(self.file, 'r') as file:
                message = file.read()

        except FileNotFoundError:
            message = f'Не найден файл: {self.file}'

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
                self.logger.error(f'Не удалось переместить лог.\nОшибка при создании папки "{dst}":\n{error}')
                return None

        dst_file = os.path.join(dst, self.filename)
        logging.shutdown()

        try:
            shutil.move(self.file, dst_file)
        except shutil.Error as error:
            self.logger.error(f'Не удалось переместить лог.\nОшибка при перемещении в {dst_file}:\n{error}')

        return None
