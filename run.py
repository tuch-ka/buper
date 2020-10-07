from buper import Buper
from logger import logger, log
from mailer import Mail


def main():
    logger.info(f'Начало резервного копирования')
    backup = Buper()

    zip_log, zip_error = backup.create_zip()

    if zip_error:
        logger.error(zip_error.decode("cp866", errors="ignore"))
        return

    logger.info(
        f'Результаты архивации:\n'
        f'{zip_log.decode("utf-8")}\n'
        f'Свободного места на диске осталось: {backup.get_free_space()} Гб'
    )

    count, list_dir = backup.delete_old_backups()
    if count:
        logger.info(f'Было удалено архивов: {count}\n{list_dir}')

    message = f'Размер архива: {backup.arch_size} Гб'
    log_text = log.read_log()

    mail = Mail(content=message, attachment=log_text)
    mail.send()

    log.move(dst=backup.folder)
        

if __name__ == '__main__':
    main()
