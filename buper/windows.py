from config.archive import conf_7z
from .base import BaseBuper


class WindowsBuper(BaseBuper):
    def _generate_command(self) -> str:
        command = f"{conf_7z.exec} a -r -spf2 -mhe {self.archive} {self.files}"

        if conf_7z.password is not None:
            command += f' -p{conf_7z.password}'
        return command

    def _files(self) -> str:
        paths = [f'"{path}"' for path in self._generate_file_paths()]
        return ' '.join(paths)
