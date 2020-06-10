import util.django
import click
from ui import ui
from pathlib import Path
import toml
import re
from typing import Dict
from dataclasses import dataclass, field
from collections import namedtuple

@dataclass
class DjangoConfig():
    project: str = 'tarot_juicer'
    app: str = 'generators'
    model: str = 'Generator'
    models: Dict = field(default_factory=dict)
    tables: list = field(default_factory=list)

    def __str__(self):
        out = f"""
        [django]
        project: {self.project}
        app: {self.app}
        model: {self.model}"""
        return out


@dataclass
class Config():
    django: DjangoConfig = field(default_factory=DjangoConfig)
    database: Dict = field(default_factory=dict)
    debug: bool = False
    directory: Path = Path('.') 
    data_pragma: Dict = field(default_factory=dict)

    def __str__(self):
        line = ui.line()
        heading = ui.heading('[config]')
        out = f"""
        {line}
        {heading}
        {line}
        {self.django}
        database: {self.database}
        directory: {self.directory.resolve().as_posix()}
        """
        return out

@click.pass_context
def load_config_file(context, config_file):
    try:
        config_toml = toml.load(config_file)
        with Path(config_file).open() as config_toml:
            config_contents = toml.load(config_toml)
            # FIXME: instead of copying directory, pass into load and set after this returns
            # config_contents['django']['directory'] = context.obj.django.directory
        django_config = config_contents['django']
        context.obj.django = DjangoConfig(**django_config)
        context.obj.data_pragma = config_contents['data_pragma']
    except FileNotFoundError:
        # accept defaults
        pass


@click.pass_context
def load(context, config_file, working_directory):
    """
    Gets options from the user with sane defaults, uses helper functions get_databases, get_apps and get_models
    to intelegently extract a list of databases, apps and models from your django settings.py and manage.py
    presents user with hopefuly user friendly menu for making choices if defaults=False
    """

    load_config_file(config_file)
    context.obj.directory = Path(working_directory)
    databases = util.django.get_databases()
    context.obj.database = databases['default']
    model_data = util.django.get_model_data()

    print(context.obj)
    accept_defaults = click.confirm('Accept this config?', default=True)
    if not accept_defaults:
        # ask the questions
        context.obj.django.app = ui.multiple_choice('Which Django app?',
                util.django.get_apps(),
                title='[DJANGO APPS]')
        context.obj.django.project = ui.multiple_choice('Which Django project?',
                util.django.get_projects(),
                title='[DJANGO PROJECTS]')
        django_models = [model_name for model in model_data.values() for model_name in model.keys() if model_name]
        context.obj.django.model = ui.multiple_choice('Which model?',
                django_models,
                title='[DJANGO MODELS]')
        database_ids = list(databases.keys())
        db_choice = click.Choice(database_ids, case_sensitive=False)
        database_id = click.prompt('Which database?', default='default', show_choices=True, type=db_choice, err=True) 
        context.obj.database = databases[database_id]


    # TODO: make find all related tables down hirarchy
    app = context.obj.django.app
    model = context.obj.django.model
    selected_model_data = model_data[app][model]
    tables = list([f"{app}_{model.lower()}"])
    for foreign_key in filter(lambda field: field.fieldtype == 'ForeignKey', selected_model_data):
    	related = foreign_key.options[0][0]
    	tables.append(related.replace('.', '_').lower())
    context.obj.django.tables = tables
    # get database into config
    context.obj.django.models = model_data

    if context.obj.debug:
        print(context.obj)
        print(context.obj.django.models)
