"""
Module that loads the configuration details from a YAML file.
"""

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from dict_recursive_update import recursive_update as _update
import munch

# This is the default settings object. It is in dictionary form, but will be accessed using object notation once the
# configuration file has been loaded.
#
# i.e. processing['output'] will be processing.output instead.
_settings = {
    'processing': {
        'inputs': ['log'],
    }
}


def add_default_configuration(key, configuration):
    """
    Method call that will add default settings, should only be called before initialize event is fired off
    :param key: key to namespace the configuration settings away
    :param configuration:
    """
    _settings[key] = configuration


def load_configuration_file(file_name):
    """
    Load the requested configuration file into memory so that the rest of the application can be configured.
    :param file_name: filename to open and load settings from
    :return: object containing settings.
    """
    global _settings

    try:
        with open(file_name, 'r') as configuration_file:
            _update(_settings, load(configuration_file, Loader=Loader))
    except FileNotFoundError:
        pass

    return munch.Munch.fromDict(_settings)


def get_configuration():
    """Returns objects with unmodified settings."""
    return munch.Munch.fromDict(_settings)
