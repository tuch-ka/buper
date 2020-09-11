import json

config_file = 'settings.json'


class ConfigFromJSONFile:
    settings = json.load(open(config_file, 'r'))
