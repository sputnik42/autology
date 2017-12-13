"""Utilities for processing log files."""
import mimetypes
import datetime
import tzlocal

from collections import namedtuple

_file_processors = {}


_FileProcessor = namedtuple('FileProcessor', 'mime_type load lookup_time')
DEFAULT_FILE_PROCESSOR = _FileProcessor('undefined', lambda x: None, lambda x: default_time_getter(x))


def register_mime_type(file_extension, mime_type):
    """Register the mime types in the system library. """
    mimetypes.add_type(mime_type, file_extension)


def lookup_mime_type(file_component):
    """Lookup the mime type based on the pathlib path provided."""
    file_component = file_component.resolve()
    file_type, encoding = mimetypes.guess_type(file_component.as_uri())
    return file_type


def default_time_getter(file):
    """Return localized now when time getter not defined."""
    return tzlocal.get_localzone().localize(datetime.datetime.now())


def register_file_processor(mime_type, file_loader, time_getter=default_time_getter):
    """Register file processor for specified mime_type."""
    _file_processors[mime_type] = _FileProcessor(mime_type, file_loader, time_getter)


def get_file_processor(file):
    """Retrieve the file processor for the provided file."""
    mime_type = lookup_mime_type(file)
    return _file_processors.get(mime_type, DEFAULT_FILE_PROCESSOR)
