import os
import importlib
import re
import click
import collections
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from functools import partial
from typing import List

# TODO: def get_columns(database):
CWD = Path(os.getcwd())
GET_MODELS_SCRIPT = ((CWD / 'util/get-models.awk').as_posix())

# save typing all the parameters each time
get_model = partial(subprocess.run, capture_output=True, text=True)

@dataclass
class Field():
    name: str = ''
    fieldtype: str = ''
    options: List = field(default_factory=list) 

@click.pass_context
def get_model_data(context):
    """ Uses helper bash script to extract model data from each app's models.py file storing the result
    into a dictionary of apps, where each app is a key and its value is a list of models.  And each model
    is a list of fields.  Each field is a dictionary.
    APPS: dictionary
        {'app1': dict {...models...},
         'app2': dict {...models...}}
    MODEL: List
        ['field1': Field,
         'field2': Field,
         ...]
    FIELD: dictionary
        {'name': str,
         'type': str,
         'options': List}
    """
    model_data = dict()
    fields = list()
    for app in get_apps():
        models_py = (context.obj.directory / f'{app}/models.py').as_posix()
        models_raw = get_model([GET_MODELS_SCRIPT, models_py]).stdout.splitlines()
        fields = list()  # list of fields

        model_data[app] = dict()
        prev_model = ''
        for data in models_raw:
            if data.count('Model'):
                _, model = data.split('#')
                # there is a previous model on record and we are dealing with a new one
                if prev_model and model != prev_model:
                    # we have a new model
                    # store prev_model_name model first
                    model_data[app][prev_model] = fields
                    fields = list() # empty, ready for new model
                prev_model = model
            else:
                # we are dealing with a field
                name, fieldtype, options = data.split('#')
                opts_ = options.split(',')
                options = list()
                
                for option in opts_:
                	option = option.replace("'", "").split('=')
                	options.append(tuple(option))
                
                field = Field(name, fieldtype, options)
                fields.append(field)
        # we have looped through all data for that apps models.py
        if not model_data[app]:
            # we are dealing with a single model situatiion
            model_data[app][prev_model] = fields
    return dict(model_data) # convert back to standard dict


@click.pass_context
def get_projects(context):
    cwd = Path(context.obj.directory)
    is_project = lambda dir: len(list(dir.rglob("settings.py"))) > 0
    return [dir.name for dir in cwd.iterdir() if dir.is_dir() and is_project(dir)]


@click.pass_context
def get_apps(context):
    """
    Simple function to iterate the current directory and return list of django apps
    """
    cwd = Path(context.obj.directory)
    # simple lambda returns True if given dir is a django app, does it contain models.py
    is_app = lambda dir: len(list(dir.glob("models.py"))) > 0
    return [dir.name for dir in cwd.iterdir() if dir.is_dir() and is_app(dir)]

@click.pass_context
def get_databases(context):
    """ extracts DATABASE dictionary from django settings.py for project name aquired from manage.py """
    django_project = context.obj.django.project 
    settings_file = context.obj.directory / f'{django_project}/settings.py' 
    # settings_file = Path(f'./{django_project}/settings.py').absolute().as_posix()
    settings_spec = importlib.util.spec_from_file_location(f'{django_project}.settings', settings_file)
    settings = importlib.util.module_from_spec(settings_spec)
    settings_spec.loader.exec_module(settings)
    databases = settings.DATABASES
    return databases
