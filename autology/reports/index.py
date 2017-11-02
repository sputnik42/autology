"""Report that builds the index file."""

from autology.events import ReportingTopics
from autology.publishing import publish

_reports = []


def register_plugin():
    """
    Register for all of the required events that will be fired off by the main loop
    :return:
    """
    ReportingTopics.REGISTER_REPORT.subscribe(_end_day_processing)
    ReportingTopics.BUILD_MASTER.subscribe(_finish_processing)


def _end_day_processing(report=None):
    """Build up a list of all the report objects that have been defined."""
    _reports.append(report)


def _finish_processing():
    publish('index.html', 'index.html', reports=_reports)
