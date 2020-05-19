import os
import importlib
import re
import click
import collections
import subprocess
from pathlib import Path



# def get_columns(database):


def get_models(app):
    """
    Gets model data from models.py as dictonary for given app where the keys
    are model names, i.e. Generators and the values are a list of Fields which
    in tern are named tuples as defined Field.  This function exists so that
    we can later compare fields against current database connection to identify
    fields that were added to the models.py but not yet migrated into the db

    return dict

    Usage:
        models = get_models('generators') # generator app in this case
        # look at the first field for the Generator model
        models['Generator'][0].name
        models['Generator'][0].type
        models['Generator'][0].prop
    """
    model_data = collections.defaultdict()
    models_py = Path('.') / app / 'models.py'
    get_model_script = Path('.') / 'scripts' / 'get-models.sh'
    script_proc = subprocess.run(['sh', get_model_script.as_posix(), models_py.as_posix()], capture_output=True, text=True)
    raw_data = script_proc.stdout.splitlines()
    for data in raw_data:
        if data.count('Model'):
            _, model = data.split('#')
            model_data[model] = list()
        else:
            # TODO: split prop into list
            name, tpe, *prop = data.split('#')
            field = Field(name, tpe, prop)
            model_data[model].append(field)
    return dict(model_data) # convert back to standard dict


def get_projects():
    cwd = Path('.')
    is_project = lambda dir: len(list(dir.rglob("settings.py"))) > 0
    return [directory.name for directory in cwd.iterdir() if directory.is_dir() and is_project(directory)]


def get_apps():
    """
    Simple function to iterate the current directory and return list of django apps
    """
    cwd = Path('.')
    # simple lambda returns True if given dir is a django app, does it contain models.py
    is_app = lambda dir: len(list(dir.glob("models.py"))) > 0
    return [directory.name for directory in cwd.iterdir() if directory.is_dir() and is_app(directory)]

@click.pass_context
def get_databases(context):
    """ extracts DATABASE dictionary from django settings.py for project name aquired from manage.py """
    django_project = context.obj.django.project 
    settings_file = context.obj.django.directory + f'/{django_project}/settings.py' 
    # settings_file = Path(f'./{django_project}/settings.py').absolute().as_posix()
    settings_spec = importlib.util.spec_from_file_location(f'{django_project}.settings', settings_file)
    settings = importlib.util.module_from_spec(settings_spec)
    settings_spec.loader.exec_module(settings)
    databases = settings.DATABASES
    return databases
