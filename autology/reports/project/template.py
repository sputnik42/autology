"""Template for the project log files."""
from autology.reports.models import Template
from autology.reports.timeline.template import template_start as timeline_start, template_end as timeline_end


def register_template():
    return Template('project_base', template_start, template_end)


def template_start(**kwargs):
    post = timeline_start(**kwargs)
    post.metadata['mkl-project'] = None

    return post


def template_end(post, **kwargs):
    post = timeline_end(post, **kwargs)

    return post
