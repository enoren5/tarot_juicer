""" This script permits the user the options of filling missing database fields with lorem ipsum and
    or default supplied data i.e. image links, bullet lists.  Intelegently reads django project
    information obtained from settings.py manage.py and models.py to provide the user with a choice
    of the target project, app, database and defaults.  Aditionaly if the models.py does not match
    with the given database, that is new fields defined in the Model do not exist in the database
    these will be added.
"""
import sqlite3
import psycopg2 # used to work with postgresql
import subprocess # used for running scripts and heroku commands
import sys
import os
import django.apps
import collections # provides named tuples
import re # regex used to extract data from complex strings
import importlib # used to import and read settings.py
import dj_database_url # DELME: dont think this is needed
import toml
from config import get_config 
from ui import get_option
from attr import attrs, attrib
from attr import Factory as attr_factory
from dataclasses import dataclass, field # for our config data
from operator import itemgetter # handy for extracting fields
from faker import Faker # gives us fake data for the empty fields
from faker.providers import lorem # allows us to use a LOREM dictonary
from pathlib import Path # used to interact with filesystem
from functools import partial # set default arguments to functions

fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()



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

            self.connection = psycopg2.connect(self.database['NAME'],
                    self.database['USER'],
                    self.database['PASSWORD'],
                    self.database['HOST'],
                    self.database['PORT'])
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *exc):
        self.connection.close()

    @property
    def pragma(self):
        return self._pragma


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




if __name__ == "__main__":
    # get options 
    cfg = get_config()

