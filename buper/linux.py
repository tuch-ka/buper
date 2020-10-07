from config.archive import conf_7z
from .base import BaseBuper


class LinuxBuper(BaseBuper):
    def _generate_command(self):
        command = [conf_7z.exec, 'a', '-r', '-spf2', '-mhe', self.archive]
        command += self.files

        if conf_7z.password is not None:
            command.append(f' -p{conf_7z.password}')

        return command

    def _files(self) -> list:
        return [path for path in self._generate_file_paths()]
