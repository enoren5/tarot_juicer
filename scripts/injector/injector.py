""" This script permits the user the options of filling missing database fields with lorem ipsum and
    or default supplied data i.e. image links, bullet lists.  Intelegently reads django project
    information obtained from settings.py manage.py and models.py to provide the user with a choice
    of the target project, app, database and defaults.  Aditionaly if the models.py does not match
    with the given database, that is new fields defined in the Model do not exist in the database
    these will be added.
"""
import click
import sqlite3
import psycopg2 # used to work with postgresql
import subprocess # used for running scripts and heroku commands
import config
import toml
from pathlib import Path
from dataclasses import dataclass
from faker import Faker # gives us fake data for the empty fields
from faker.providers import lorem # allows us to use a LOREM dictonary
from functools import partial # set default arguments to functions

fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()

APP_NAME = ('injector')


""" Context for handling connection to database, works with postgres and sqlite thus far """
class TarotDatabaseConnection(object):
    def __init__(self, database_config):
        self.connection = None
        self.cursor = None
        self.database = database_config

    def __enter__(self):
        if self.database['ENGINE'].find('sqlite') != -1:
            self.connection = sqlite3.connect(self.database['NAME'])
        else:
            # assume it is postgresql
            # database, user, password, host, port 
            self.connection = psycopg2.connect(database=self.database['NAME'],
                    user = self.database['USER'],
                    password = self.database['PASSWORD'],
                    host = self.database.get('HOST', 'localhost'),
                    port = self.database.get('PORT', 5432))
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *exc):
        self.connection.close()

    def columns(self, table):
        self.cursor.execute(f'select * from {table} limit 0')
        return list(desc[0] for desc in self.cursor.description)


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

@click.command()
@click.option('--conf', type=click.Path(exists=True, dir_okay=False, file_okay=True), help='configuration file')
@click.option('--debug/--no-debug', type=bool, default=False)
@click.argument('directory', type=click.Path(exists=True,  file_okay=False, resolve_path=True))
@click.pass_context
def main(context, conf, debug, directory):
    # get options 
    # context.ensure_object(dataclass)
    if not conf:
        cwd_config = Path('config.toml')
        if cwd_config:
            config_file = cwd_config.resolve().as_posix()
        else:
            config_directory = click.get_app_dir(APP_NAME)
            config_file = config_directory + 'config.toml'
     
    context.obj = config.Config()
    context.obj.debug = debug
    config.load(config_file, directory)


if __name__ == "__main__":
    main(obj={})
