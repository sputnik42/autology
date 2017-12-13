"""Simple template definition for a log file that contains start time, end time, location, and empty content."""
from datetime import datetime
import tzlocal

import frontmatter

from autology.reports.timeline import keys as fm_keys
from autology.reports.models import Template
import pkg_resources

PACKAGE_NAME = 'autology'


def register_template():
    return Template('timeline_base', template_start, template_end)


def template_start():
    """ Start a new file template based on the content of the template definition. """

    _post = frontmatter.Post('', **{
        fm_keys.TIME: tzlocal.get_localzone().localize(datetime.now()),
        fm_keys.END_TIME: None,
        fm_keys.LOCATION: 'home',
        fm_keys.AGENT_DEFINITION: {
            fm_keys.AGENT_NAME: PACKAGE_NAME,
            fm_keys.AGENT_VERSION: pkg_resources.require(PACKAGE_NAME)[0].version,
            fm_keys.FILE_VERSION: '{}'.format(fm_keys.CURRENT_FILE_VERSION)
        }
    })
    return _post


def template_end(post):
    """
    Finish the manipulation of the metadata in the front matter before saving the contents to the storage engine.
    :param post: the post file that will be modified.
    """
    if not post.metadata[fm_keys.END_TIME]:
        post.metadata[fm_keys.END_TIME] = tzlocal.get_localzone().localize(datetime.now())

    # Time value is currently stored in a different timezone, so make sure that it's set to the local timezone value
    # just as the end time is
    if fm_keys.TIME in post.metadata:
        post.metadata[fm_keys.TIME] = post.metadata[fm_keys.TIME].astimezone(tzlocal.get_localzone())

    return post
