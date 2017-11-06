"""
Provides wrapper around common publishing functionality.
"""
import pathlib
from jinja2 import Environment, FileSystemLoader
from autology import topics
from autology.configuration import add_default_configuration, get_configuration

_environment = None
_output_path = None


def register_plugin():
    """
    Subscribe to the initialize method and add default configuration values to the settings object.
    :return:
    """
    topics.Application.INITIALIZE.subscribe(_initialize)

    add_default_configuration('publishing',
                              {
                                  'templates': 'templates',
                                  'output': 'output'
                              })


def _initialize():
    """
    Initialize the jinja environment.
    :return:
    """
    global _environment, _output_path
    configuration_settings = get_configuration()

    # Load the same jinja environment for everyone
    _environment = Environment(
        loader=FileSystemLoader(configuration_settings.publishing.templates)
    )

    # Verify that the output directory exists before starting to write out the content
    _output_path = pathlib.Path(configuration_settings.publishing.output)
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
