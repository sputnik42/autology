"""
Module that loads the configuration details from a YAML file.
"""

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


settings = {
    'processing': {
        'inputs': ['log'],
        'output': 'output',
        'templates': 'templates'
    }
}


def load_configuration_file(file_name):
    """
    Load the requested configuration file into memory so that the rest of the application can be configured.
    :param file_name:
    :return:
    """
    global settings

    try:
        with open(file_name, 'r') as configuration_file:
            settings.update(load(configuration_file, Loader=Loader))
    except FileNotFoundError:
        pass

    return settings
