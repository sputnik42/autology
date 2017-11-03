"""
Events that are used in the publish subscription values.
"""
import enum
from pubsub import pub


class PubSubEnumMixin:
    """Mixin that allows for the enumerations to publish and subscribe themselves."""

    def subscribe(self, listener):
        return pub.subscribe(listener, self.value)

    def publish(self, **kwargs):
        pub.sendMessage(self.value, **kwargs)


@enum.unique
class Processing(PubSubEnumMixin, enum.Enum):
    """
    Enumeration that defines the lifecycle of processing the collection of files in the logs.
    DAY_START -
      parameters: date - datetime.date object for the day that is being processed.
    DAY_END -
      parameters: date - datetime.date object for the day that was processed.
    PROCESS_FILE -
      parameters:
        file - the file that should be looked over.
        date - the date that the file was saved in.
    BEGIN -
      Event that is fired off before processing files.
      parameters: none
    END -
      Event that is fired off when all of the files have been processed.
      parameters: none
    """
    DAY_START = 'day_start'
    DAY_END = 'day_end'
    PROCESS_FILE = 'process_file'
    BEGIN = 'begin'
    END = 'end'


@enum.unique
class Reporting(PubSubEnumMixin, enum.Enum):
    """
    Topics related to notifying of new reports based on the processed data.

    REGISTER_REPORT -
      parameters: report definition named tuple
    BUILD_MASTER -
      parameters: none
    """
    REGISTER_REPORT = 'register_report'
    BUILD_MASTER = 'build_master'
