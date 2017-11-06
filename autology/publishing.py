"""
Provides wrapper around common publishing functionality.
"""
import pathlib
from jinja2 import Environment, FileSystemLoader

_environment = None
_output_path = None


def initialize(configuration_settings):
    """
    Initialize the jinja environment.
    :param configuration_settings:
    :return:
    """
    global _environment, _output_path

    # Load the same jinja environment for everyone
    _environment = Environment(
        loader=FileSystemLoader(configuration_settings.processing.templates)
    )

    # Verify that the output directory exists before starting to write out the content
    _output_path = pathlib.Path(configuration_settings.processing.output)
    _output_path.mkdir(exist_ok=True)


def publish(template, output_file, context=None, **kwargs):
    """
    Notify jinja to publish the template to the output_file location with all of the context provided.
    :param template:
    :param output_file:
    :param context:
    :param kwargs:
    :return:
    """
    if not context:
        context = {}

    context.update(kwargs)

    root_template = _environment.get_template(str(template))
    output_content = root_template.render(context)
    output_file = pathlib.Path(_output_path, output_file)

    # Verify that the path is possible.
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(output_content)
