"""
    Модуль логики резервного копирования
    TODO: ротация файлов бэкапа
    TODO: архивирование с использованием 7z
"""

import os
import shutil

from time import time

from settings import base, backup


def get_path_list() -> list:
    """
    Составляет список папок, которые:
        -   не входят в игнор лист
        -   содержат в себе файлы с искомым расширением
    """
    paths = []

    for root, folders, files in os.walk(base['folder']):
        folders[:] = [folder for folder in folders if folder not in base['ignore']]

        already_exist = False
        for path in paths:
            if root.startswith(path):
                already_exist = True
                break
        if already_exist:
            continue

        for file in files:
            if file.endswith(base['extension']):
                paths.append(root)
                # TODO: добавлять папки или файлы. Если файлы, то убрать проверку наличия папки в paths
                break

    return paths


def zip_files(src):
    pass


def backup_rotation() -> tuple:
    """ Удаляет папки архива старше заданного количества дней
        Возвращает кортеж, в котором:
            элемент с индексом [0] - количество удалённых папок
            элемент с индексом [1] - список удалённых папок
    """
    list_dir = []                           # Список удалённых папок
    count = 0                               # Счетчик удалённых папок

    if backup['lifetime'] < 1 or backup['count'] < 1 or not os.path.exists(backup['folder']):
        return count, list_dir

    # Отсчет заданного количества дней от текщего аремени, в секундах (86400 - кол-во секунд в сутках)
    lifetime = time() - (backup['lifetime'] * 86400)

    for folder in os.listdir(backup['folder']):
        folder_path = os.path.join(backup['folder'], folder)

        if os.path.isdir(folder_path):
            if os.path.getmtime(folder_path) < lifetime:
                shutil.rmtree(folder_path, ignore_errors=True)

                if os.path.exists(folder_path):
                    # TODO: log error
                    print(f'error {folder_path}')
                    continue
                # TODO: log
                print(f'good {folder_path}')
                list_dir.append(folder_path)
                count += 1
            else:   # TODO: debug info
                print(f'young {folder_path}')
        else:   # TODO: debug info
            print(f'not dir {folder_path}')

    return count, list_dir


def get_free_space() -> float:
    """
    Возращает размер свободного пространста на disk в гигабайтах
    """
    stat = shutil.disk_usage(backup['folder'])
    return round((stat[2] / 1024 ** 3), 2)


if __name__ == '__main__':
    print(f'Будут запакованы: {get_path_list()}')
    print(f'Свободно на диске: {get_free_space()} Гб')
    backup_rotation()

