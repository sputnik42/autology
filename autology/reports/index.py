"""Report that builds the index file."""

import pathlib
from autology import topics
from autology.publishing import publish

_reports = []

INDEX_TEMPLATE_PATH = pathlib.Path('index', 'index.html')


def register_plugin():
    """ Subscribe to the initialize method and add default configuration values to the settings object. """
    topics.Application.INITIALIZE.subscribe(_initialize)


def _initialize():
    """ Register for all of the required events that will be fired off by the main loop """
    topics.Reporting.REGISTER_REPORT.subscribe(_new_report_handler)
    topics.Reporting.BUILD_MASTER.subscribe(_finish_processing)


def _new_report_handler(report=None):
    """Build up a list of all the report objects that have been defined."""
    _reports.append(report)


def _finish_processing():
    publish(INDEX_TEMPLATE_PATH, 'index.html', reports=_reports)
