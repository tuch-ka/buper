"""
    Модуль логики резервного копирования
"""

import os
import shutil
import subprocess

from datetime import datetime
from time import time

from settings import base, backup, arch
from mail import send_mail
from log import get_log, move_logs

log = get_log()
DATE = (datetime.now()).strftime("%Y-%m-%d")
BACKUP_FOLDER = os.path.join(backup['folder'], DATE)


def get_path_list() -> str:
    """
    Составляет список папок, которые не входят в игнор лист
    """
    paths = ''
    root = os.path.normpath(base['folder'])
    ext = base["extension"]

    folders = os.listdir(root)
    folders[:] = [
        folder
        for folder in folders
        if folder not in base['ignore']
    ]

    for folder in folders:
        folder_path = os.path.join(root, folder)
        if os.path.isdir(folder_path):
            paths += f'"{folder_path}\\*{ext}" '
    return paths


def zip_files(src: str):
    """ Архивирует архив
    """
    destination = os.path.join(BACKUP_FOLDER, DATE + '.7z')
    command = f"{arch['exec']} a -spf2 -mhe {destination} {src} -p{arch['password']}"
    result = subprocess.run(command, capture_output=True)
    return result.stdout, result.stderr, destination


def backup_rotation() -> tuple:
    """ Удаляет папки архива старше заданного количества дней
        Возвращает кортеж, в котором:
            элемент с индексом [0] - количество удалённых папок
            элемент с индексом [1] - список удалённых папок
    """
    list_dir = []                           # Список удалённых папок
    count = 0                               # Счетчик удалённых папок

    if backup['lifetime'] < 1 or backup['count'] < 1 or not os.path.exists(backup['folder']):
        log.info(
            f"Ротация архивов не выполнена:\n"
            f"lifetime: {backup['lifetime']}\n"
            f"count: {backup['count']}\n"
            f"folder: {backup['folder']}"
        )
        return count, list_dir

    # Отсчет заданного количества дней от текщего аремени, в секундах (86400 - кол-во секунд в сутках)
    lifetime = time() - (backup['lifetime'] * 86400)

    for folder in os.listdir(backup['folder']):
        folder_path = os.path.join(backup['folder'], folder)

        if os.path.isdir(folder_path):
            if os.path.getmtime(folder_path) < lifetime:
                shutil.rmtree(folder_path, ignore_errors=True)

                if os.path.exists(folder_path):
                    log.error(f'Удаление старого архива не удалось: {folder_path}')
                    continue
                list_dir.append(folder_path)
                count += 1

    return count, list_dir


def get_free_space() -> float:
    """
    Возращает размер свободного пространста на disk в гигабайтах
    """
    stat = shutil.disk_usage(backup['folder'])
    return round((stat[2] / 1024 ** 3), 2)


def main():
    log.info(f'Начало резервного копирования')

    folders_to_archive = get_path_list()
    log.info(f"Список файлов для архивации:\n{folders_to_archive}")

    zip_log, zip_error, arch_file = zip_files(folders_to_archive)
    if zip_error:
        log.error(zip_error.decode("cp866", errors="ignore"))
        return ''
    log.info(
        f'Результаты архивации:\n'
        f'{zip_log.decode("utf-8")}\n'
        f'Свободного места на диске осталось: {get_free_space()} Гб'
    )

    count, list_dir = backup_rotation()
    log.info(f'Было удалено архивов: {count}\n{list_dir}')

    arch_size = round((float(os.path.getsize(arch_file)) / 1024 ** 3), 2)
    send_mail(f'Размер архива: {arch_size} Гб')
    move_logs(BACKUP_FOLDER)


if __name__ == '__main__':
    pass

