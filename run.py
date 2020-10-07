from buper import Buper
from logger import logger, log
from mailer import Mail
from config import MAX_CAPACITY


def main():
    logger.info('Начало резервного копирования')
    backup = Buper()

    zip_message, zip_error = backup.create_zip()

    if zip_error is not None:
        logger.error(zip_error)
        mail_message = 'Ошибка архивации!'

    else:
        mail_message = f'Размер архива: {backup.arch_size} Гб'

        capacity = backup.check_disk_capacity()
        if capacity < MAX_CAPACITY + 1:
            logger.warning(f'На диске осталось {backup.free_space} Гб')
            logger.warning(f'Места хватит для {capacity} архивов')
            mail_message += f'\nВНИМАНИЕ! Заканчивается место!'

        logger.info('Результаты архивации:')
        logger.info(zip_message)

        count, list_dir = backup.delete_old_backups()
        if count:
            logger.info(f'Было удалено архивов: {count}\n{list_dir}')

    mail_log = log.read_log()

    mail = Mail(content=mail_message, attachment=mail_log)
    mail.send()

    logger.info('Конец резервного копирования')
    log.move(dst=backup.folder)


if __name__ == '__main__':
    main()
