"""Processes the front data in the markdown files to process project stat recordings."""
import frontmatter
from autology import topics
from yaml import load_all
import datetime
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from dict_recursive_update import recursive_update as _r_update

# Constants:
DEFAULT_PROJECT_LENGTH = 60  # minutes


# This is a dictionary containing all of the defined projects, they key is a project identifier that is defined when
# defining the project. Inside should be a dictionary containing a key of datetime object for an entry, and then the
# entry that is associated with that project.
_defined_projects = {}
_defined_organizations = {}
_defined_customers = {}


def register_project_plugin():
    """Register the subscribers for the project plugin."""
    topics.Processing.PROCESS_FILE.subscribe(_process_file)
    topics.Processing.END.subscribe(_dump_data_structures)


def _dump_data_structures():
    print('Defined Projects: {}'.format(_defined_projects))
    print('Defined Organizations: {}'.format(_defined_organizations))
    print('Defined Customers: {}'.format(_defined_customers))


def _process_file(file, date):
    """
    Process the file.

    This will subscribe to markdown files, which it will use to record the amount of time that the event is taking
    place.  For YAML files it will will look for root object definitions that it understands.  These will have the
    key:  mkl-project and will contain some kind of project identifier.

    It is not guaranteed that the files that are being processed will be processed in order.
    """
    if file.suffix == '.md':
        _process_markdown(file, date)
    elif file.suffix == '.yaml':
        _process_yaml(file=file)


def _process_markdown(file, date):
    """Process the front-matter contents, and store the markdown if necessary."""
    post = frontmatter.load(file)

    if not post.keys():
        return

    _process_yaml(frontmatter=post.metadata)

    if 'mkl-project' in post.metadata and not isinstance(post['mkl-project'], dict):

        # Then is clearly must be a string
        project_definition = _defined_projects.setdefault(post['mkl-project'], {})
        project_log = project_definition.setdefault('log', {})

        time = file.stem
        hours = time[0:2]
        minutes = time[2:]

        time = datetime.time(int(hours), int(minutes))
        log_date = datetime.datetime.combine(date, time)
        project_log[log_date] = project_definition

        # Calculate how long the event lasts TODO: probably should be in a utility
        time_on_project = project_definition.get('duration', datetime.timedelta())

        if 'end_time' in post.metadata and post['end_time'] is not None:
            end_time_hours = post['end_time'][0:2]
            end_time_minutes = post['end_time'][3:]
            end_time = datetime.datetime.combine(date, datetime.time(int(end_time_hours), int(end_time_minutes)))
            duration = end_time - log_date
        else:
            duration = datetime.timedelta(minutes=DEFAULT_PROJECT_LENGTH)

        project_definition['duration'] = time_on_project + duration


def _process_yaml(file=None, frontmatter=None):
    """Process the documents in a yaml file and update data structures according to the data values."""

    # Create a valid documents variable based on the parameters that are provided.
    if file:
        with open(file) as yaml_file:
            documents = [d for d in load_all(yaml_file, Loader=Loader)]
    elif frontmatter:
        documents = [frontmatter]
    else:
        documents = []

    for document in documents:

        # Figure out if any of the documents contain definitions of project/organization/customers and if so, see if
        # the documents define them (i.e. have dictionaries), or if the document is just about the data.
        if 'mkl-project' in document:

            project_definition = document['mkl-project']
            if not isinstance(project_definition, dict):
                continue

            definition_collection = _defined_projects
            updated_definition = project_definition

        elif 'mkl-organization' in document:

            organization_definition = document['mkl-organization']
            if not isinstance(organization_definition, dict):
                continue

            definition_collection = _defined_organizations
            updated_definition = organization_definition

        elif 'mkl-customer' in document:

            customer_definition = document['mkl-customer']
            if not isinstance(customer_definition, dict):
                continue

            definition_collection = _defined_customers
            updated_definition = customer_definition

        else:
            continue

        # Update the values in the previous definition, otherwise it is the new definition.  This is because the
        # definition_collection may already contain some values from files before (i.e. received markdown files about
        # working on the project before the definition yaml file was processed).
        previous_definition = definition_collection.setdefault(updated_definition['id'], {})
        _r_update(previous_definition, updated_definition)
