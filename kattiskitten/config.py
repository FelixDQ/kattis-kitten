import configparser
import os
from pathlib import Path

config_path = os.path.join(Path.home(), '.kattiskitten', 'config.ini')

cfg = configparser.ConfigParser()
cfg.read(config_path)


def get(key, section='DEFAULT'):
    return cfg[section][key] if key in cfg[section] else None

def set(key, value, section='DEFAULT'):
    if section not in cfg:
        cfg[section] = {}
    cfg[section][key] = value

    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))

    with open(config_path, 'w') as file:
        cfg.write(file)

def sectionExists(section):
    return True if section in cfg else False