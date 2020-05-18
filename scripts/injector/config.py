import util
from ui import option_prompt
from pathlib import Path
import toml
import re
from attr import attrs, attrib
from attr import Factory as attr_factory
from collections import namedtuple
import importlib

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

    def __str__(self):
        attr_str_(self)
        
    

@attrs
class HerokuConfig():
    project = attrib(default='tarot-juicer-in-production')

    def __str__(self):
        attr_str_(self)
    

@attrs
class Config():
    django = attrib(default=attr_factory(DjangoConfig))
    heroku = attrib(default=attr_factory(HerokuConfig))
    database = attrib(default=attr_factory(dict))
    models = attrib(default=attr_factory(dict))

    def __str__(self):
        attr_str_(self)


def load_config_file(file='injector.toml'):
    try:
        with Path(CONFIG_FILE).open() as config_toml:
            config = toml.load(config_toml)
            CONFIG.django = DjangoConfig(**config['django'])
            CONFIG.heroku = HerokuConfig(**config['heroku'])
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
        django_models = util.django.get_models().keys()
        CONFIG.django.project = option_prompt(django_projects, 
                'Which Django project?',
                show_menu=True,
                title='[DJANGO PROJECTS]')
        CONFIG.django.app = option_prompt(django_apps,
                'Which Django app?',
                show_menu=True,
                title='[DJANGO APPS]')
        CONFIG.django.model = option_prompt(django_models,
                'Which Model are we targeting?',
                show_menu=True,
                title='[MODEL]')


    # get database into config
        
    databases = util.django.get_databases(CONFIG.django.project)
    database_id = option_prompt(databases.keys(), 'Which database are we working with?', show_menu=True, title='[DATABASES]')
    CONFIG.database = databases[database_id]
    CONFIG.models = util.django.get_models(CONFIG.django.app)
    


    # not using defaults, ask the user questions
    # if not defaults:
    #     confirm_project = 'no'
    #     while confirm_project == 'no':
    #         confirm_project = get_option(['yes', 'no'], f'is {config.heroku_project} the heroku project name?')
    #         if confirm_project != 'yes':
    #             config.heroku_project = input('What is the name of the heroku project? ')
    #     config.database = get_database_config(heroku_project, default=False)
    #     django_apps = get_apps()
    #     config.django_app = get_option(django_apps, f'What is our django app? ', title='[APPS]')
    #     config.models = get_models(config.django_app)
    #     config.model = get_option(list(config.models.keys()), 'Which model do you want? ', title='[MODELS]')
    # else:
    #     config.models = get_models(config.django_app)
    #     config.database = get_database_config(config.heroku_project, default=True)

    # if verbose:
    #     print('')
    #     menu('[CONFIGURATION]')
    #     print(config)

    return config
