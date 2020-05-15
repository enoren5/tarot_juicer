""" This script permits the user the options of filling missing database fields with lorem ipsum and
    or default supplied data i.e. image links, bullet lists.  Intelegently reads django project
    information obtained from settings.py manage.py and models.py to provide the user with a choice
    of the target project, app, database and defaults.  Aditionaly if the models.py does not match
    with the given database, that is new fields defined in the Model do not exist in the database
    these will be added.
"""
import sqlite3
import subprocess # used for running scripts and heroku commands
import sys
import os
import django.apps
import collections # provides named tuples
import re # regex used to extract data from complex strings
import importlib # used to import and read settings.py
import dj_database_url # DELME: dont think this is needed
from dataclasses import dataclass, field # for our config data
from operator import itemgetter # handy for extracting fields
from faker import Faker # gives us fake data for the empty fields
from faker.providers import lorem # allows us to use a LOREM dictonary
from pathlib import Path # used to interact with filesystem
from functools import partial # set default arguments to functions

fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()

@dataclass
class Config:
    """ configuration data for script :: change defaults here """
    database: dict = field(default_factory=dict,metadata = {'description': 'dictionary from settings.DATABASES'})
    heroku_project: dict = field(default='tarot-juicer-in-production', metadata = {'description': 'name of heroku app'})
    django_app: str = field(default='generators', metadata = {'description': 'name of django app not project'})
    model: str = field(default='Generator', metadata = {'description': 'model that we want to inject into'})
    models: dict = field(default_factory=dict, metadata = {'description': 'nested dictionary with model data extracted from models.py'})
    # TODO: make default factory
    table: str = field(default='generators_Generator', metadata = {'description': 'table name in database to inject into'})

    def __str__(self):
        self_describe = ''
        if 'NAME' in self.database:
            self_describe += f'Database: {self.database["NAME"]}\n'
        else:
            self_describe += f'Database: unknown\n'
        self_describe += f'Heroku App: {self.heroku_project}\n'
        self_describe += f'Django App: {self.django_app}\n'
        self_describe += f'Model: {self.model}\n'
        return self_describe

# type to hold field data from models
Field = collections.namedtuple('Field', 'name type properties')

def tarotDatabaseConnection(database_config):
    """ function to create and return database connection """
    if (database_config.type == 'sqlite'):
        return 
    else:
        pass

def bullets(num_bullets, words_per):
    """ generates <num_bullets> ammount of lorem ipsum bullets """
    return "\n".join(
        fake.sentence(nb_words=words_per, ext_word_list=LOREM, variable_nb_words=False)
        for _ in range(num_bullets)
    )

# various lorem ipsum generators preconfigured as partials
paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)
clear_screen = partial(subprocess.call, 'clear')

line = lambda width: print('=' * width)

def get_database_config(heroku_project, default=True, menu='[SELECT DATABASE]'):
    """ extracts DATABASE dictionary from django settings.py for project name aquired from manage.py """
    manage_file = Path('.') / 'manage.py'
    # read manage.py
    with manage_file.open() as manage_py:    
        raw_manage = manage_py.readlines()

    # get the project name via regex
    django_project = re.search(r"\'(\w+\.settings)\'", ''.join(raw_manage)).group(1)

    # use trick to execute settings.py, asuming its location is not known, project name subject to change 
    settings_file = re.sub(r'\.', '/', django_project) + '.py'
    settings_spec = importlib.util.spec_from_file_location(django_project, settings_file)
    settings_module = importlib.util.module_from_spec(settings_spec)
    settings_spec.loader.exec_module(settings_module)
    databases = settings_module.DATABASES # get DATABASES from settings.py

    database_id = 'default' if default else get_option([db_id for db_id in databases.keys()], 'Which database should we use?')
    database = databases[database_id]
    fields = ['USER', 'PASSWORD', 'HOST', 'PORT']
    name = database['NAME']
    engine = database['ENGINE']

    if not name:
        """ blank name means heroku database but we are not running this script inside heroku environment / dyno 
            : use regex to extract data from DATABASE_URL via heroku config:get"""
        database_url = subprocess.run(['heroku', 'config:get', 'DATABASE_URL', '-a', heroku_project], capture_output=True, text=True).stdout
        data = re.match(r"postgres:\W{2}(\w+):(\w+)@(.+):(\d*)\/(\w+)", database_url).groups()
        data = dict(zip(fields + ['NAME'], data))
        return data
    
    # if field missing set it to empty string
    for field in fields:
        if field not in database:
            if field == 'PORT':
                if engine.find('postgresql') != -1:
                    if field in database:
                        database[field] = databases.get(database_id)['PORT']
                    else:
                        database[field] = os.getenv('PGPORT') or 4532
                else:
                    database[field] = 0 # not used by sqlite
                continue
            elif field == 'HOST':
                if engine.find('sqlite') != -1:
                    database[field] = 'localhost'
                    continue
            else:
                database[field] = ''

    return database


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


def menu(title, width = 80):
    """
    Prints fancy menu
    """
    print('\n')
    line(width)
    print(f'{title:^{width}}')
    line(width)


def get_apps():
    """
    Simple function to iterate the current directory and return list of django apps
    """
    cwd = Path('.')
    # simple lambda returns True if given dir is a django app, does it contain models.py
    is_app = lambda dir: len(list(dir.glob("models.py"))) > 0
    return [directory.name for directory in cwd.iterdir() if directory.is_dir() and is_app(directory)]


def get_option(options, prompt, title='MENU'):
    """
    Gets value for option from user input via prompt and loops until 'a' or valid option

    Parameters:
        options : List
            list of valid options, first item is default
        prompt : prompt
            prompt text to use for input
    """
    options.append('Abort!') 
    prompt += " ==> "
    choice =  len(options) + 1 # invalid choice gets loop started 
    valid_choices = [str(i) for i in range(1, len(options) + 1)]
    while choice not in valid_choices:
        # clear_screen()
        # print menu
        menu(title)
        # show the options
        for i, option in enumerate(options):
            print(f'{i+1}: {option}')
        print('\n')
        choice = input(prompt)
        if choice == '':
            choice = '1'
            break
        elif int(choice) == len(options):
            sure = input('Are you sure? [y,n] ')
            if sure == 'y':
                sys.exit() # aborting
            else:
                choice='x'

    # value will be false if its empty, aka default first option 
    return options[int(choice) - 1] if choice else options[0]


def config(verbose=False, defaults=True):
    """
    Gets options from the user with sane defaults, uses helper functions get_databases, get_apps and get_models
    to intelegently extract a list of databases, apps and models from your django settings.py and manage.py
    presents user with hopefuly user friendly menu for making choices if defaults=False
    """
    heroku_project = 'tarot-juicer-in-production' # default
    cfg = dict(database=get_database_config(heroku_project),
            app='generators', # target app 
            model='Generator', # target model
            models=get_models('generators'),
            table='',
            )
    config = Config()

    # not using defaults, ask the user questions
    if not defaults:
        confirm_project = 'no'
        while confirm_project == 'no':
            confirm_project = get_option(['yes', 'no'], f'is {config.heroku_project} the heroku project name?')
            if confirm_project != 'yes':
                config.heroku_project = input('What is the name of the heroku project? ')
        config.database = get_database_config(heroku_project, default=False)
        django_apps = get_apps()
        config.django_app = get_option(django_apps, f'What is our django app? ', title='[APPS]')
        config.models = get_models(config.django_app)
        config.model = get_option(list(config.models.keys()), 'Which model do you want? ', title='[MODELS]')
    else:
        config.models = get_models(config.app)
        config.database = get_database_config(config.heroku_project, default=True)

    if verbose:
        print('')
        menu('[CONFIGURATION]')
        print(config)

    return config

if __name__ == "__main__":
    # get options
    cfg = config(verbose=True, defaults=False)
