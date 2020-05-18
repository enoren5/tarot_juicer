import util
from ui import option_prompt
from pathlib import Path
import toml
import re
from attr import attrs, attrib
from attr import Factory as attr_factory
from collections import namedtuple

CONFIG_FILE = ('injector.toml')
CONFIG = Config() # start with default

# type to hold field data from models
Field = namedtuple('Field', 'name type properties')

def attr_str_(obj):
    str = ''
    for attr in dir(obj):
        if re.match(r"^[A-Za-z]", attr):
            str += f"{attr} = {getattr(obj, attr)}\n"
    return str



@attrs
class DjangoConfig():
    project = attrib(default='tarot_juicer')
    app = attrib(default='generators')
    model = attrib(default='Generator')
    models = attrib(default=attr_factory(dict))

    def __str__(self):
        attr_str_(self)
        

@attrs
class Config():
    django = attrib(default=attr_factory(DjangoConfig))
    database = attrib(default=attr_factory(dict))

    def __str__(self):
        attr_str_(self)


def load_config_file(file='injector.toml'):
    try:
        with Path(CONFIG_FILE).open() as config_toml:
            config = toml.load(config_toml)
            CONFIG.django = DjangoConfig(**config['django'])
    except FileNotFoundError:
        # accept defaults
        pass


def config():
    """
    Gets options from the user with sane defaults, uses helper functions get_databases, get_apps and get_models
    to intelegently extract a list of databases, apps and models from your django settings.py and manage.py
    presents user with hopefuly user friendly menu for making choices if defaults=False
    """
    load_config_file()
    print(CONFIG)
    make_changes = option_prompt(['Yes', 'No'], 'Make changes?', show_menu=False)
    if make_changes == 'Yes':
        # ask the questions
        django_projects = util.django.get_projects()
        django_apps = util.django.get_apps()
        CONFIG.django.project = option_prompt(django_projects, 
                'Which Django project?',
                show_menu=True,
                title='[DJANGO PROJECTS]')
        CONFIG.django.app = option_prompt(django_apps,
                'Which Django app?',
                show_menu=True,
                title='[DJANGO APPS]')
        django_models = util.django.get_models(CONFIG.django.app).keys()
        CONFIG.django.model = option_prompt(django_models,
                'Which Model are we targeting?',
                show_menu=True,
                title='[MODEL]')


    # get database into config
    databases = util.django.get_databases(CONFIG.django.project)
    database_id = option_prompt(databases.keys(), 'Which database are we working with?', show_menu=True, title='[DATABASES]')
    CONFIG.database = databases[database_id]
    CONFIG.django.models = util.django.get_models(CONFIG.django.app)
