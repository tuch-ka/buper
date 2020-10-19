from buper import Buper
from logger import log
from mailer import Mail


def main():
    logger = log.logger
    logger.info('Начало резервного копирования')
    backup = Buper()

    zip_message, zip_error = backup.create_zip()

    if zip_error is not None:
        logger.error(zip_error)
        mail_message = 'Ошибка архивации!'

    else:
        mail_message = f'Размер архива: {backup.arch_size} Гб'

        logger.info('Результаты архивации:')
        logger.info(zip_message)

        count, list_dir = backup.delete_old_backups()
        if count:
            logger.info(f'Было удалено архивов: {count}\n{list_dir}')

        capacity = backup.check_disk_capacity()
        if not capacity:
            logger.warning(f'На диске осталось {backup.free_space} Гб')
            mail_message += f'\nВНИМАНИЕ! Заканчивается место! Свободно {backup.free_space} Гб'

    mail_log = log.read_log()

    mail = Mail(content=mail_message, attachment=mail_log)
    mail.send()

    logger.info('Конец резервного копирования')
    log.move(dst=backup.folder)


if __name__ == '__main__':
    main()
