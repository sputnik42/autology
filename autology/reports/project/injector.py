from autology.utilities import injectors, log_file
import pathlib


def register_injector():
    injectors.register_injector('mkl-project', handle_injection)


def handle_injection(file=None, date=None):

    if file is None:
        print('Cannot handle null file')

    injection_file = pathlib.Path(file)

    # TODO: If the file is a YAML file, load up the template for base project and inject the yaml content into the
    # definition and use the metadata from the template as the metadata in front matter.
