"""
Events that are used in the publish subscription values.
"""
import enum
from pubsub import pub


class PubSubEnumMixin:
    def subscribe(self, listener):
        return pub.subscribe(listener, self.value)

    def publish(self, **kwargs):
        pub.sendMessage(self.value, **kwargs)


@enum.unique
class ProcessingTopics(PubSubEnumMixin, enum.Enum):

    DAY_START = 'day_start'
    DAY_END = 'day_end'

    PROCESS_FILE = 'process_file'


