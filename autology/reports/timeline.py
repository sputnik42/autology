"""
Timeline report that will process all of the files into a timeline in order to be published to the log.
"""
import datetime

import frontmatter
import markdown

from autology.reports.models import Report
from autology.events import ProcessingTopics, ReportingTopics
from autology.publishing import publish

# The current date that is being processed.
_current_date = datetime.date.today()

# The content that is stored for each individual day
_day_content = []

# Dates that have been collected
_dates = []


def register_plugin():
    """
    Register for all of the required events that will be fired off by the main loop
    :return:
    """
    ProcessingTopics.DAY_START.subscribe(_start_day_processing)
    ProcessingTopics.PROCESS_FILE.subscribe(_data_processor)
    ProcessingTopics.DAY_END.subscribe(_end_day_processing)
    ProcessingTopics.END.subscribe(_end_processing)


def _start_day_processing(date=None):
    """
    Event handler that will be notified when a day's files are starting to be processed.
    :param date: the day that is being processed.
    :return:
    """
    global _day_content, _current_date
    _day_content = []
    _current_date = date
    _dates.append(date)


def _data_processor(file=None):
    """
    Checks to see if the data can be processed and stores any data required locally.
    :param file:
    :return:
    """
    if file.suffix != '.md':
        return

    time = file.stem
    hours = time[0:2]
    minutes = time[2:]

    post = frontmatter.load(file)
    time = datetime.time(int(hours), int(minutes))

    _day_content.append((datetime.datetime.combine(_current_date, time), post.content))


def _end_day_processing(date=None):
    """Publish the content of the collated day together."""
    # Now output the content has html so that it can be rendered
    markdown_conversion = markdown.Markdown()
    markdown_result = ''
    for content_day, content in sorted(_day_content, key=lambda x: x[0]):
        markdown_result += markdown_conversion.reset().convert(content)

    publish('day.html', "{:04d}{:02d}{:02d}.html".format(_current_date.year, _current_date.month,
                                                         _current_date.day), content=markdown_result)


def _end_processing():
    publish('timeline_report.html', 'timeline_report.html', dates=_dates)
    ReportingTopics.REGISTER_REPORT.publish(report=Report('Timeline', 'List of all report files',
                                                          'timeline_report.html'))
