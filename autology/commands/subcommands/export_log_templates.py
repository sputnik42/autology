"""Sub-command that will create a new note file for the log."""
import frontmatter
from pkg_resources import iter_entry_points

from autology.configuration import get_configuration_root


def register_command(subparser):
    """Register the subcommand with any additional arguments."""
    parser = subparser.add_parser('export_log_templates', help='Export the defined log templates to a directory')
    parser.set_defaults(func=_main)

    parser.add_argument('--output-dir', '-o', help='Location to output all of the templates to',
                        default='templates/generation')


def _main(args):
    """
    Create a new note file in the correct location.
    :param args:
    :return:
    """
    loaded_templates = {}

    for ep in iter_entry_points(group='autology_templates'):
        template_object = ep.load()()

        if not isinstance(template_object, list):
            template_object = [template_object]

        for to in template_object:
            loaded_templates[to.name] = to

    output_directory = get_configuration_root() / args.output_dir

    for name, template in loaded_templates.items():
        output_file = output_directory / "{}.md".format(name)

        post = template.start()

        output_file.write_text(frontmatter.dumps(post))
