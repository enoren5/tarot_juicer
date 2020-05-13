import sqlite3
import subprocess
import numpy
import pandas
import sys
import django.apps
import collections
import re
import importlib
import dj_database_url
from operator import itemgetter
from faker import Faker
from faker.providers import lorem
from pathlib import Path
from functools import partial


fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()

""" function to create and return database connection intelegently from first reading settings.py """
def tarotDatabaseConnection(database):
    print(f'database: {database}')

def bullets(num_bullets, words_per):
    return "\n".join(
        fake.sentence(nb_words=words_per, ext_word_list=LOREM, variable_nb_words=False)
        for _ in range(num_bullets)
    )


paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)
clear_screen = partial(subprocess.call, 'clear')
line = lambda width: print('=' * width)

""" extracts DATABASE dictionary from django settings.py for project name aquired from manage.py
"""
def get_databases():
    manage_file = Path('.') / 'manage.py'
    # read manage.py
    with manage_file.open() as manage_py:    
        raw_manage = manage_py.readlines()
    # get the project name via regex
    project = re.search(r"\'(\w+\.settings)\'", ''.join(raw_manage)).group(1)
    # use trick to execute settings.py, because we asume project name is unknown and thus not imported
    project_file = re.sub(r'\.', '/', project) + '.py'
    spec = importlib.util.spec_from_file_location(project, project_file)
    project_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(project_module)
    databases = project_module.DATABASES
    return databases

# def get_columns(database):


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
def get_models(app):
    Field = collections.namedtuple('Field', 'name type prop')
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
            name, tpe, *prop = data.split('#')
            field = Field(name, tpe, prop)
            model_data[model].append(field)
    return dict(model_data) # convert back to standard dict


"""
Prints fancy menu
"""
def menu(title, width = 80):
    print('\n')
    line(width)
    print(f'{title:^{width}}')
    line(width)


"""
Simple function to iterate the current directory and return list of django apps
"""
def get_apps():
    cwd = Path('.')
    # simple lambda returns True if given dir is a django app, does it contain models.py
    is_app = lambda dir: len(list(dir.glob("models.py"))) > 0
    return [directory.name for directory in cwd.iterdir() if directory.is_dir() and is_app(directory)]


"""
Gets value for option from user input via prompt and loops until 'a' or valid option

Parameters:
    options : List
        list of valid options, first item is default
    prompt : prompt
        prompt text to use for input
"""
def get_option(options, prompt, title='MENU'):
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


"""
Gets options from the user with sane defaults, uses helper functions get_databases, get_apps and get_models
to intelegently extract a list of databases, apps and models from your django settings.py and manage.py
presents user with hopefuly user friendly menu for making choices if defaults=False
"""
def config(verbose=False, defaults=True):
    DATABASE = collections.namedtuple('DATABASE', 'id config')
    # so we can connect to it.  name is database, secret is password
    DATABASE_CFG = collections.namedtuple('DATABASE_CFG', 'name host port user secret type')
    databases = get_databases()
    cfg = dict(database=DATABASE('default', databases.get('default')),
            project='tarot-juicer-in-production', # heroku app name, used if we connect to heroku
            app='generators', # target app 
            model='Generator', # target model
            models=get_models('generators'),
            table='',
            )
    # not using defaults, ask the user questions
    if not defaults:
        database_id = get_option([db for db in databases.keys()], 'Which database should we use?')
        database = DATABASE(database_id, databases.get(database_id))
        confirm_project = 'no'
        while confirm_project == 'no':
            confirm_project = get_option(['yes', 'no'], f'is {cfg.get("project")} the project name?')
            if confirm_project != 'yes':
                cfg['project'] = input('What is the name of the heroku project? ')

        apps = get_apps()
        app = get_option(apps, f'What is our django app? ', title='[APPS]')
        cfg['models'] = get_models(app)
        model = get_option(list(cfg.get('models').keys()), 'Which model do you want? ', title='[MODELS]')
    else:
        database, project,  app, model = itemgetter('database', 'project', 'app', 'model')(cfg)
   
    """so far the cfg['database'].config contains a dictionary of unuseful django stuff, mostly missing hostnames
    , replace it with useful connection specs needed to establish a connection with python"""
    is_heroku = get_option(['Yes', 'No'], f'is {database.id} a heroku postgres database?', title='[HEROKU/LOCAL]')
    if is_heroku == 'Yes':
        database_url = subprocess.run(['heroku', 'config:get', 'DATABASE_URL', '-a', cfg.get('project')], capture_output=True, text=True).stdout
        user, secret, host, port, name = re.match(r"postgres:\W{2}(\w+):(\w+)@(.+):(\d*)\/(\w+)",tr).groups()
        database.config = DATABASE_CFG(name, host, port, user, secret, 'postgresql')
    # else do we have a local postgresql
    elif database.config.get('ENGINE').find('postgresql') != -1:
        user, secret, name = itemgetter('USER', 'PASSWORD', 'NAME')(database.config)
        host = 'localhost'
        port = database.config.get('PORT') or os.getenv('PGPORT') or 4532
        database.config = DATABASE_CFG(name, host, port, user, secret, 'postgresql')
    # assume sqlite, and not encrypted with SQLCipher
    else:
        name = database.config.get('NAME') #  should be full path to db.sqlite3 file
        host = database.config.get('HOST') or '' # usualy empty, if not use sockets
        database.config = DATABASE_CFG(name, host, 0, '', '', 'sqlite') 
        

    cfg['database'] = database
    cfg['app'] = app
    cfg['model'] = model
    cfg['table'] = f'{app}_{model}'.lower() # django uses lowercalse <app>_<model>

    if verbose:
        print('')
        menu('[CONFIGURATION]')
        for option in cfg.keys():
            if option == 'database':
                print(f'{option}: {cfg.get(option).id}')
            else:
                print(f'{option}: {cfg.get(option)}')

    return cfg

if __name__ == "__main__":
    # get options
    cfg = config(verbose=True, defaults=False)
