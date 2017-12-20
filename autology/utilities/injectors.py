"""
Module that will allow developers to register their injection methods into inject command.  Each plugin can only
inject a single receiver.  From the content that is provided, the method will have to farm out it's own functionality.
These calls should be made during the plugin registration method.
"""

_INJECTORS = {}


def register_injector(_key, _callable):
    """Register the injector based on the key and callable method."""
    global _INJECTORS
    _INJECTORS[_key] = _callable


def get_injector(_key):
    """Retrieved the registered injector."""
    return _INJECTORS.get(_key, None)
