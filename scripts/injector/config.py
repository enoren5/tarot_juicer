import util.django
import click
from ui import option_prompt, heading, line
from pathlib import Path
import toml
import re
from typing import Dict
from dataclasses import dataclass, field
from collections import namedtuple

@dataclass
class DjangoConfig():
    directory: str = ''
    project: str = 'tarot_juicer'
    app: str = 'generators'
    model: str = 'Generator'
    models: Dict = field(default_factory=dict)

    def __str__(self):
        out = '[django]\n'
        out += line(80) 
        out += f"""
        directory: {self.directory}
        project: {self.project}
        app: {self.app}
        model: {self.model}"""
        return out
        
        


@dataclass
class Config():
    django: DjangoConfig = field(default_factory=DjangoConfig)
    database: Dict = field(default_factory=dict)
    debug: bool = False

    def __str__(self):
        out = heading('[config]', verbose=False)
        out += f"""{self.django}
        database: {self.database}
        """
        return out

@click.pass_context
def load_config_file(context, config_file):
    try:
        config_toml = toml.load(config_file)
        with Path(config_file).open() as config_toml:
            config_contents = toml.load(config_toml)
        context.obj.django = DjangoConfig(**config_contents['django'])
    except FileNotFoundError:
        # accept defaults
        pass

# type to hold field data from models
Field = namedtuple('Field', 'name type properties')

@click.pass_context
def load(context, config_file):
    """
    Gets options from the user with sane defaults, uses helper functions get_databases, get_apps and get_models
    to intelegently extract a list of databases, apps and models from your django settings.py and manage.py
    presents user with hopefuly user friendly menu for making choices if defaults=False
    """

    load_config_file(config_file)
    databases = util.django.get_databases()
    context.obj.database = databases['default']
    print(context.obj)
    accept_defaults = click.confirm('Accept this config?', default=True)
    if not accept_defaults:
        # ask the questions
        django_projects = util.django.get_projects()
        django_apps = util.django.get_apps()
        context.obj.django.project = option_prompt(django_projects, 
                'Which Django project?',
                show_menu=True,
                title='[DJANGO PROJECTS]')
        context.obj.django.app = option_prompt(django_apps,
                'Which Django app?',
                show_menu=True,
                title='[DJANGO APPS]')
        django_models = list(util.django.get_models(context.obj.django.app).keys())
        context.obj.django.model = option_prompt(django_models,
                'Which Model are we targeting?',
                show_menu=True,
                title='[MODEL]')
        database_ids = list(databases.keys())
        db_choice = click.Choice(database_ids, case_sensitive=False)
        database_id = click.prompt('Which database?', default='default', show_choices=True, type=db_choice, err=True) 
        context.obj.database = databases[database_id]


    # get database into config
    context.obj.django.models = util.django.get_models(context.obj.django.app)

    if context.obj.debug:
        print(context.obj)
