import argparse
import datetime
import pathlib

from autology.configuration import load_configuration_file as _load_configuration_file
from autology.events import ProcessingTopics, ReportingTopics
from autology.publishing import initialize as initialize_publishing


def _build_arguments():

    parser = argparse.ArgumentParser(description='Execute autology root command')
    parser.add_argument('--config', '-c', action='store', default='config.yaml',)

    return parser.parse_args()


def _load_plugins():
    from autology.reports.timeline import register_plugin as register_timeline_plugin
    from autology.reports.index import register_plugin as register_index_plugin
    register_timeline_plugin()
    register_index_plugin()


def main():
    args = _build_arguments()
    _load_plugins()

    configuration_settings = _load_configuration_file(args.config)
    initialize_publishing(configuration_settings)

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

    ProcessingTopics.BEGIN.publish()

    # Now need to process each of the files in order, and build up a master static page for the content.
    for year in sorted(sorted_files.keys()):
        month_files = sorted_files[year]

        for month in sorted(month_files.keys()):
            day_files = month_files[month]

            for day in sorted(day_files.keys()):
                time_files = day_files[day]

                date_to_process = datetime.date(year, month, day)
                ProcessingTopics.DAY_START.publish(date=date_to_process)

                for content_file in time_files:
                    ProcessingTopics.PROCESS_FILE.publish(file=content_file)

                dates.append(date_to_process)
                ProcessingTopics.DAY_END.publish(date=date_to_process)

    ProcessingTopics.END.publish()

    ReportingTopics.BUILD_MASTER.publish()


if __name__ == '__main__':
    main()
