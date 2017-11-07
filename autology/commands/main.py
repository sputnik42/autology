import argparse
import datetime
import pathlib

from autology.configuration import load_configuration_file as _load_configuration_file
from autology import topics


def _build_arguments():

    parser = argparse.ArgumentParser(description='Execute autology root command')
    parser.add_argument('--config', '-c', action='store', default='config.yaml',)

    return parser.parse_args()


def _load_plugins():
    from pkg_resources import iter_entry_points

    for ep in iter_entry_points(group='autology_plugins'):
        ep.load()()


def main():
    args = _build_arguments()

    # Load the plugins and allow them to set default properties in the configuration data object.
    _load_plugins()

    # Override the default values in configuration with the values from settings file.
    configuration_settings = _load_configuration_file(args.config)

    # Initialize all of the plugins in the architecture now that the settings have been loaded
    topics.Application.INITIALIZE.publish()

    sorted_files = {}

    # Need to find all of the files that are stored in the input_files directories in order to start building the
    # reports that will be used to generate the static log files.
    for input_path in configuration_settings.processing.inputs:
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

    topics.Processing.BEGIN.publish()

    # Now need to process each of the files in order, and build up a master static page for the content.
    for year in sorted(sorted_files.keys()):
        month_files = sorted_files[year]

        for month in sorted(month_files.keys()):
            day_files = month_files[month]

            for day in sorted(day_files.keys()):
                time_files = day_files[day]

                date_to_process = datetime.date(year, month, day)
                topics.Processing.DAY_START.publish(date=date_to_process)

                for content_file in time_files:
                    topics.Processing.PROCESS_FILE.publish(file=content_file, date=date_to_process)

                dates.append(date_to_process)
                topics.Processing.DAY_END.publish(date=date_to_process)

    topics.Processing.END.publish()

    topics.Reporting.BUILD_MASTER.publish()

    topics.Application.FINALIZE.publish()


if __name__ == '__main__':
    main()
