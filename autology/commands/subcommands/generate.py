"""Sub command that will generate the content of the static site."""
import datetime
import pathlib
import mimetypes
import tzlocal

from autology import topics
from autology.configuration import get_configuration
from autology.utilities import log_file


def register_command(subparser):
    """Register the sub-command with any additional arguments."""
    generator_parser = subparser.add_parser('generate', help='Generate the static content')
    generator_parser.set_defaults(func=_main)


def _main(args):
    configuration_settings = get_configuration()

    sorted_files = {}

    # Need to find all of the files that are stored in the input_files directories in order to start building the
    # reports that will be used to generate the static log files.
    for input_path in configuration_settings.processing.inputs:
        search_path = pathlib.Path(input_path)

        for file_component in search_path.glob('**/*'):

            if not file_component.is_dir():
                file_processor = log_file.get_file_processor(file_component)

                if file_processor:
                    entry = file_processor.load(file_component)
                    entry_time = file_processor.lookup_time(entry)

                    storage = sorted_files.setdefault(entry_time.year, {})
                    storage = storage.setdefault(entry_time.month, {})
                    storage.setdefault(entry_time.day, []).append(file_component)

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
                    try:
                        topics.Processing.PROCESS_FILE.publish(file=content_file, date=date_to_process)
                    except:
                        import traceback
                        print('Exception raised while processing: {}'.format(content_file))
                        traceback.print_exc()

                dates.append(date_to_process)
                topics.Processing.DAY_END.publish(date=date_to_process)

    topics.Processing.END.publish()

    topics.Reporting.BUILD_MASTER.publish()
