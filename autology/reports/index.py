"""Report that builds the index file."""

from autology import topics
from autology.publishing import publish

_reports = []


def register_plugin():
    """
    Register for all of the required events that will be fired off by the main loop
    :return:
    """
    topics.Reporting.REGISTER_REPORT.subscribe(_new_report_handler)
    topics.Reporting.BUILD_MASTER.subscribe(_finish_processing)


def _new_report_handler(report=None):
    """Build up a list of all the report objects that have been defined."""
    _reports.append(report)


def _finish_processing():
    publish('index.html', 'index.html', reports=_reports)
