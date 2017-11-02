"""Report that builds the index file."""

from autology.events import ProcessingTopics
from autology.publishing import publish

_dates = []


def register_plugin():
    """
    Register for all of the required events that will be fired off by the main loop
    :return:
    """
    ProcessingTopics.DAY_END.subscribe(_end_day_processing)
    ProcessingTopics.END.subscribe(_finish_processing)


def _end_day_processing(date=None):
    """Build up a list of all the dates that have been processed so that the index can be built."""
    _dates.append(date)


def _finish_processing():
    publish('index.html', 'index.html', dates=_dates)
