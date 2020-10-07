import os
import shutil
import subprocess
from datetime import datetime
from time import time

from config.backup import conf_backup
from logger import logger


class BaseBuper:

    def __init__(self):
        self.date = (datetime.now()).strftime("%Y-%m-%d")
        self.folder = os.path.join(conf_backup.dst, self.date)
        self.archive = os.path.join(self.folder, self.date + '.7z')

        self.files = self._files()
        self.arch_size = None

    def get_free_space(self) -> float:
        """
        Возращает размер свободного пространста в гигабайтах
        """
        statistic = shutil.disk_usage(self.folder)
        return round((statistic[2] / 1024 ** 3), 2)

    def create_zip(self) -> tuple:
        """
        Формирует и исполняет команду для 7z
        """
        command = self._generate_command()

        logger.debug(f'Zip command: {command}')

        try:
            result = subprocess.run(command, capture_output=True)
            self.arch_size = round((float(os.path.getsize(self.archive)) / 1024 ** 3), 2)
        except Exception as e:
            return '', e
        return result.stdout, result.stderr

    def _generate_command(self):
        """
        Формирует команду запуска архиватора в зависимости от ОС
        """
        raise NotImplemented

    @staticmethod
    def delete_old_backups():
        """ Удаляет папки архива старше заданного количества дней
            Возвращает кортеж, в котором:
                элемент с индексом [0] - количество удалённых папок
                элемент с индексом [1] - список удалённых папок
        """
        list_dir = []  # Список удалённых папок
        count = 0  # Счетчик удалённых папок

        if not conf_backup.lifetime or not conf_backup.count or not os.path.exists(conf_backup.dst):
            logger.info(
                f"Ротация архивов не выполнена:\n"
                f"lifetime: {conf_backup.lifetime}\n"
                f"count: {conf_backup.count}\n"
                f"folder: {conf_backup.dst}"
            )
            return count, list_dir

        # Отсчет заданного количества дней от текщего аремени, в секундах (86400 - кол-во секунд в сутках)
        lifetime = time() - (conf_backup.lifetime * 86400)

        for folder in os.listdir(conf_backup.dst):
            folder_path = os.path.join(conf_backup.dst, folder)

            if os.path.isdir(folder_path):
                if os.path.getmtime(folder_path) < lifetime:
                    shutil.rmtree(folder_path, ignore_errors=True)

                    if os.path.exists(folder_path):
                        logger.error(f'Удаление старого архива не удалось: {folder_path}')
                        continue
                    list_dir.append(folder_path)
                    count += 1

        return count, list_dir

    def _files(self) -> list:
        raise NotImplemented

    @staticmethod
    def _generate_file_paths():
        for path, folders, files in os.walk(conf_backup.src):
            for ignored in conf_backup.ignore:
                if ignored in folders:
                    folders.remove(ignored)

            for file in files:
                if file not in conf_backup.ignore:
                    yield os.path.join(path, file)
