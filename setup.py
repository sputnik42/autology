from setuptools import find_packages, setup

setup(
    name='autology',
    version='0.1',
    packages=find_packages(),
    url='',
    license='BSD 3 Clause',
    author='Robert Robinson',
    author_email='rerobins@meerkatlabs.org',
    description='File-based life log',
    entry_points={
        'console_scripts': ['autology=autology.commands.main:main'],
        'autology_plugins': ['index_report=autology.reports.index:register_plugin',
                             'timeline_report=autology.reports.timeline:register_plugin',
                             'project_report=autology.reports.project:register_plugin',
                             'publishing=autology.publishing:register_plugin'],
        'autology_commands': ['generate=autology.commands.subcommands.generate:register_command']
    }
)
