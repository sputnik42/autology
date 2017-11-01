import argparse
import datetime
import pathlib

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

from autology.configuration import load_configuration_file as _load_configuration_file


def _build_arguments():

    parser = argparse.ArgumentParser(description='Execute autology root command')
    parser.add_argument('--config', '-c', action='store', default='config.yaml',)

    return parser.parse_args()


def main():
    args = _build_arguments()

    configuration_settings = _load_configuration_file(args.config)

    sorted_files = {}

    # Need to find all of the files that are stored in the input_files directories in order to start building the
    # reports that will be used to generate the static log files.
    for input_path in configuration_settings['processing']['inputs']:
        search_path = pathlib.Path(input_path)

        # Currently going to make the assumption that everyone is using the path naming convention that I'm dictating
        # which is YYYY/MM/DD/file.ext

        for file_component in search_path.glob('*/*/*/*'):
            # Store all of the files into a dictionary containing the keys and a list of the files that are associated
            # with that day
            year, month, day = file_component.parent.relative_to(search_path).parts

            storage = sorted_files.setdefault(int(year), {})
            storage = storage.setdefault(int(month), {})
            storage.setdefault(int(day), []).append(file_component)

    dates = []

    # Now need to process each of the files in order, and build up a master static page for the content.
    for year in sorted(sorted_files.keys()):
        month_files = sorted_files[year]
        for month in sorted(month_files.keys()):
            day_files = month_files[month]
            for day in sorted(day_files.keys()):
                # Hand the content over to the handlers that will generate the content which will then be stored
                # in a list ordered by timestamps.

                time_files = day_files[day]

                day_content = []
                for content_file in time_files:
                    if content_file.suffix == '.md':
                        time = content_file.stem
                        hours = time[0:2]
                        minutes = time[2:]

                        post = frontmatter.load(content_file)

                        day_content.append((datetime.datetime(year, month, day, int(hours), int(minutes)),
                                            post.content))

                # Now output the content has html so that it can be rendered
                markdown_conversion = markdown.Markdown()
                markdown_result = ''
                for content_day, content in sorted(day_content, key=lambda x: x[0]):
                    markdown_result += markdown_conversion.reset().convert(content)

                # Render the content through jinja and save it off to a file.
                env = Environment(
                    loader=FileSystemLoader(configuration_settings['processing']['templates'])
                )
                template = env.get_template('day.html')
                output_content = template.render(content=markdown_result)

                # Save the file off to the filesystem
                output_path = pathlib.Path(configuration_settings['processing']['output'])
                output_path.mkdir(exist_ok=True)

                output_file = pathlib.Path(configuration_settings['processing']['output'],
                                           "{:04d}{:02d}{:02d}.html".format(year, month, day))
                output_file.write_text(output_content)

                dates.append(datetime.date(year, month, day))

    # Have to process the main template as well
    env = Environment(
        loader=FileSystemLoader(configuration_settings['processing']['templates'])
    )
    root_template = env.get_template('index.html')
    output_content = root_template.render(dates=dates)
    output_file = pathlib.Path(configuration_settings['processing']['output'], 'index.html')
    output_file.write_text(output_content)


if __name__ == '__main__':
    main()
