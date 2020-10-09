from config.archive import conf_7z
from .base import BaseBuper
from logger import log


class LinuxBuper(BaseBuper):
    def _generate_command(self) -> list:
        command = [conf_7z.exec, 'a', '-r', '-spf2', '-mhe', self.archive]
        command += self.files

        if conf_7z.password is not None:
            command.append(f' -p{conf_7z.password}')

        log.logger.debug(f'Сформированная команда для архиватора:\n{command}')
        return command

    def _files(self) -> list:
        paths = [path for path in self._generate_file_paths()]
        log.logger.debug(f'Отобрано файлов для архивации: {len(paths)}')
        log.logger.debug(paths)
        return paths
