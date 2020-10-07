import json
import os

# Минимальное количество архивов, для которых должно оставаться место на диске
MAX_CAPACITY = 3

# Конфигурационный файл
config_file = 'settings.json'


class ConfigFromJSONFile:
    if os.path.exists(config_file):
        settings = json.load(open(config_file, 'r'))
    else:
        settings = dict()
