import os
import shutil
import subprocess
from datetime import datetime
from time import time
from typing import Tuple, Union, Generator

from config.backup import conf_backup
from logger import logger


class BaseBuper:

    def __init__(self):
        self.date = (datetime.now()).strftime("%Y-%m-%d")
        self.folder = os.path.join(conf_backup.dst, self.date)
        self.archive = os.path.join(self.folder, self.date + '.7z')

        self.files = self._files()
        self.arch_size = None

    def create_zip(self) -> Tuple[str, Union[Exception, str, None]]:
        """
        Выполняет команду для 7z.
        Возвращает консольный вывод и ошибку.
        """
        command = self._generate_command()

        logger.debug(f'Zip command: {command}')

        try:
            result = subprocess.run(command, capture_output=True)

            if result.stderr:
                response = ''
                error = result.stderr.decode("cp866", errors="ignore")

            else:
                response = result.stdout.decode("utf-8")
                error = None
                self.arch_size = round((float(os.path.getsize(self.archive)) / 1024 ** 3), 2)

        except Exception as e:
            response = ''
            error = e

        return response, error

    def get_free_space(self) -> float:
        """
        Возращает размер свободного пространста в гигабайтах
        """
        statistic = shutil.disk_usage(self.folder)
        return round((statistic[2] / 1024 ** 3), 2)

    def delete_old_backups(self) -> Tuple[int, list]:
        """ Удаляет папки архива старше заданного количества дней, если они указаны
            Возвращает кортеж, в котором:
                элемент с индексом [0] - количество удалённых папок
                элемент с индексом [1] - список удалённых папок
        """

        if not conf_backup.lifetime or not conf_backup.count or not os.path.exists(conf_backup.dst):
            logger.info(
                f"Ротация архивов не выполнена:\n"
                f"lifetime: {conf_backup.lifetime}\n"
                f"count: {conf_backup.count}\n"
                f"folder: {conf_backup.dst}"
            )
            return 0, []

        return self._remove_old()

    @staticmethod
    def _remove_old() -> Tuple[int, list]:
        """
        Производит удаление старых архивов
        """
        count = 0       # Счетчик удалённых папок
        list_dir = []   # Список удалённых папок

        # Отсчет заданного количества дней от текщего аремени, в секундах (86400 - кол-во секунд в сутках)
        max_lifetime = time() - (conf_backup.lifetime * 86400)

        for folder in os.listdir(conf_backup.dst):
            folder_path = os.path.join(conf_backup.dst, folder)
            folder_lifetime = os.path.getmtime(folder_path)

            if os.path.isdir(folder_path) and folder_lifetime < max_lifetime:

                try:
                    shutil.rmtree(folder_path)
                    list_dir.append(folder_path)
                    count += 1

                except shutil.Error as error:
                    logger.error(f'Удаление старого архива не удалось: {folder_path}\n{error}')

        return count, list_dir

    @staticmethod
    def _generate_file_paths() -> Generator:
        for path, folders, files in os.walk(conf_backup.src):
            for ignored in conf_backup.ignore:
                if ignored in folders:
                    folders.remove(ignored)

            for file in files:
                if file not in conf_backup.ignore:
                    yield os.path.join(path, file)

    def _generate_command(self):
        """
        Формирует команду запуска архиватора в зависимости от ОС
        """
        raise NotImplemented

    def _files(self):
        """
        Адаптирует список файлов из метода _generate_file_paths для метода _generate_command в зависимости от ОС
        """
        raise NotImplemented
