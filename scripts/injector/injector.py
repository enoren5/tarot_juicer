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


@click.pass_context
def find_new_fields(context, table=None, model=None):
    """ function to locate columns that exist in the model but not yet in the database table for
    the model.

    :param table: database table to check against
    :type table: str, optional
    :param model: django model name to check for new columns
    :type model: str, optional
    :return: A list of new columns that exist in the model that are absent from the database
    :rtype: list

    """
    table = table or context.obj.django.table
    model = model or context.obj.django.model
    app = context.obj.django.app
    model_data = context.obj.django.models[app][model]
    # model_columns = get_models()
    with TarotDatabaseConnection(context.obj.database) as tarot_db:
        db_columns = tarot_db.columns(table)
    new_fields = list()
    for field in model_data:
        if field.name not in db_columns:
            new_fields.append(field)
    return new_fields


# various lorem ipsum generators preconfigured as partials
paragraph = partial(
    fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True
)
word = partial(fake.word, ext_word_list=LOREM)
clear_screen = partial(subprocess.call, 'clear')

@click.command()
@click.option('--conf', type=click.Path(exists=True, dir_okay=False, file_okay=True), help='configuration file')
@click.option('--data', type=click.File(lazy=True), help='initial data sql file to inject')
@click.option('--debug/--no-debug', type=bool, default=False)
@click.argument('directory', type=click.Path(exists=True,  file_okay=False, resolve_path=True))
@click.pass_context
def main(context, conf, debug, directory):
    # context.ensure_object(dataclass)
    if not conf:
        cwd_config = Path('config.toml')
        if cwd_config:
            config_file = cwd_config.resolve().as_posix()
        else:
            config_directory = click.get_app_dir(APP_NAME)
            config_file = config_directory + 'config.toml'

    # build configuration object
    context.obj = config.Config()
    context.obj.debug = debug
    config.load(config_file, directory)

    table = context.obj.django.table
    with TarotDatabaseConnection(context.obj.database) as tarot_db:
        #: new_fields: fields that are defined in the model that dont exist in database table
        new_fields = find_new_fields(table)

        column_names = tarot_db.columns(table)
        tarot_db.cursor.execute(f'SELECT * FROM  {table} WHERE NOT ({table} IS NOT NULL)')
        null_records = tarot_db.cursor.fetchall()
        null_fields = list()

        # build list of fields containing null values
        if len(null_records) > 0:
            for record in null_records:
                for field_name, field in zip(column_names, record):
                    if not field:
                        null_fields.append(field_name)
        else:
            null_fields = column_names
        #: fake_generators: maps fake types to their apropriate generator
        fake_generators = {
                'lorem word': word,
                'lorem paragraph': paragraph,
                'bullets': bullets(6, 3)
                }
        #: fake_types: click choice , list of fake types to choose from
        fake_types = click.Choice(fake_generators.keys(), case_sensitive=False)
        #: fake_map: maps which fake generator to use for each field 
        fake_map = dict()
        #: list of tuples (field.name, field.value)
        record_values = list()
        # ask user what fake data to use for each null field / column
        for field in null_fields:
            fake_type = click.prompt(f'Type for {field}', type=fake_types, show_choices=True)
            fake_map[field] = fake_generators.get(fake_type)

        # read in the ddl 
        try:
            with Path('./ddl.toml').open() as ddl_file:
                ddl = toml.load(ddl_file)
        except:
            click.echo('DDL is missing, cannot add new columns... continuing without')



        # add new columns :: manual migration
        if ddl:
            engine = context.obj.database['ENGINE'].split('.')[-1]
            for field in new_fields:
                sql_type = context.obj.django.models[field.fieldtype][engine]
                tarot_db.cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {sql_type}')

        if data:
            # run the sql insert into sql file
            tarot_db.cursor.execute(data.read())

        # grab all the records
        tarot_db.cursor.execute(f'SELECT * FROM {table}')
        records = tarot_db.cursor.fetchall()
        if len(records) > 0:
            do_drop = click.confirm('drop current records?', default=False, show_default=True)
            if do_drop:
                tarot_db.cursor.execute(f'DELETE FROM {table}')
            for record in records:
                for field_name, field_value in zip(column_names, record):
                    if field_name == 'id':
                        record_id = field_value
                        continue
                    elif not field_value:
                        # append fake data to values, call the generator
                        value = fake_map.get(field_name)()
                    else:
                        # use existing value
                        value = field_value
                    sql_update = f'update {table} set {field_name} = %s where id = %s'
                    tarot_db.execute(sql_update, (field_name, value, ))
            tarot_db.connection.commit()


if __name__ == "__main__":
    main(obj={})
