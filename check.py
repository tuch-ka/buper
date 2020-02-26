import os
from settings import *


def check_settings() -> bool:

    if not isinstance(BASE_1C, str):
        print(r"BASE_1C должен быть строкой формата r'диск:\\' либо r'полный_путь_к_папке_без_последнего_слэша'")
        return False
    elif not os.path.exists(BASE_1C):
        print("BASE_1C не найден")
        return False

    if not isinstance(EXTENSION_1C, str) or not EXTENSION_1C.startswith('.'):
        print(r"EXTENSION_1C должен быть строкой формата r'.расширение'")
        return False

    if not isinstance(IGNORE, list) or not all(isinstance(ignore, str) for ignore in IGNORE):
        print(r"IGNORE должен быть списком строк формата ['dir1', 'dir2', ]")
        return False

    if not isinstance(BACKUP_FOLDER, str):
        print(r"BASE_1C должен быть строкой формата r'полный_путь_к_папке_без_последнего_слэша'")
        return False

    if not isinstance(BACKUP_COUNT, int) or BACKUP_COUNT < 0:
        print(r"BACKUP_COUNT должен быть числом больше либо равным нулю")
        return False

    if not isinstance(BACKUP_LIFETIME, int) or BACKUP_LIFETIME < 0:
        print(r"BACKUP_LIFETIME должен быть числом больше либо равным нулю")
        return False

    if not isinstance(ARCH_PASSWORD, str):
        print(r"ARCH_PASSWORD должен быть стройкой. Отсутствие пароля - пустая строка ''")
        return False

    if not isinstance(ARCH_EXEC, str):
        print(r"ARCH_EXEC должен быть стройкой формата r'полный_путь_к_7z.exe'")
        return False
    elif not os.path.exists(ARCH_EXEC):
        print(f'Исполняемый файл архиватора {ARCH_EXEC} не найден')
        return False

    if not isinstance(LOG_FOLDER, str):
        print(r"LOG_FOLDER должен быть стройкой. Если не важно - пустая строка '', "
              r"лог в любом случае будет перемещаться в папку с архивом")
        return False

    if not isinstance(LOG_FILENAME, str):
        print("LOG_FILENAME должен быть строкой 'имя_файла'")
        return False

    return True


if __name__ == '__main__':
    if check_settings():
        print('Всё хорошо')
