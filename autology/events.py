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
class ProcessingTopics(PubSubEnumMixin, enum.Enum):
    """
    Enumeration that defines the lifecycle of processing the collection of files in the logs.

    DAY_START -
      parameters: date - datetime.date object for the day that is being processed.
    DAY_END -
      parameters: date - datetime.date object for the day that was processed.
    PROCESS_FILE -
      parameters: file - the file that should be looked over.
    """
    DAY_START = 'day_start'
    DAY_END = 'day_end'
    PROCESS_FILE = 'process_file'
