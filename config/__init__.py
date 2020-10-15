import json
import os

# Конфигурационный файл
config_file = 'settings.json'


class ConfigFromJSONFile:
    if os.path.exists(config_file):
        settings = json.load(open(config_file, 'r'))
    else:
        settings = dict()
