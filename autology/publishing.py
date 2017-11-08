"""
Provides wrapper around common publishing functionality.
"""
import pathlib
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from autology import topics
from autology.configuration import add_default_configuration, get_configuration

_environment = None
_output_path = None
_markdown_conversion = None


def register_plugin():
    """
    Subscribe to the initialize method and add default configuration values to the settings object.
    :return:
    """
    topics.Application.INITIALIZE.subscribe(_initialize)

    add_default_configuration('publishing',
                              {
                                  'templates': 'templates',
                                  'output': 'output',
                                  'url_root': '/'
                              })


def _initialize():
    """
    Initialize the jinja environment.
    :return:
    """
    global _environment, _output_path, _markdown_conversion
    configuration_settings = get_configuration()

    # Create markdown conversion object
    _markdown_conversion = markdown.Markdown()

    # Load the same jinja environment for everyone
    _environment = Environment(
        loader=FileSystemLoader(configuration_settings.publishing.templates),
        autoescape=select_autoescape()
    )

    # Load up the custom filters
    _environment.filters['autology_url'] = url_filter
    _environment.filters['markdown'] = markdown_filter

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
    output_file = _output_path / output_file

    # Verify that the path is possible.
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(output_content)


def url_filter(url):
    """Filter that will prepend the URL root for links in order to put the log in a directory on a webserver."""
    config = get_configuration()
    if config.publishing.url_root:
        return "{}{}".format(get_configuration().publishing.url_root, url)
    return url


def markdown_filter(content):
    """Filter that will translate markdown content into HTML for display."""
    return _markdown_conversion.reset().convert(content)
