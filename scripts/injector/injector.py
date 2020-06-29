""" This script permits the user the options of filling missing database fields with lorem ipsum and
	or default supplied data i.e. image links, bullet lists.  Intelegently reads django project
	information obtained from settings.py manage.py and models.py to provide the user with a choice
	of the target project, app, database and defaults.  Aditionaly if the models.py does not match
	with the given database, that is new fields defined in the Model do not exist in the database
	these will be added.
"""
import click
import sqlite3
import psycopg2  # used to work with postgresql
import subprocess  # used for running scripts and heroku commands
import config
import toml
import random
import csv
from itertools import count
from pathlib import Path
from dataclasses import dataclass
from faker import Faker  # gives us fake data for the empty fields
from faker.providers import lorem  # allows us to use a LOREM dictonary
from functools import partial  # set default arguments to functions


fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

LOREM = "Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split()
APP_NAME = ('injector')


class TarotDatabaseConnection(object):
	""" Context for handling connection to database, works with postgres and sqlite thus far """
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
												user=self.database['USER'],
				password=self.database['PASSWORD'],
				host=self.database.get('HOST', 'localhost'),
				port=self.database.get('PORT', 5432))
		self.cursor = self.connection.cursor()
		return self


	def __exit__(self, *exc):
		self.connection.close()


	def columns(self, table):
		self.cursor.execute(f'select * from {table} limit 0')
		return list(desc[0] for desc in self.cursor.description)


def bullets(num_bullets = 5, words_per = 6):
	""" generates <num_bullets> ammount of lorem ipsum bullets """
	return "\n".join(
		fake.sentence(nb_words=words_per, ext_word_list=LOREM,
						variable_nb_words=False)
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


def number(min=1, max=99): return random.randrange(min, max)
boolean = lambda: True

thumbnail = lambda x: f"thumbnails/K{0 if x in range(1, 10) else ''}{x}.jpg"
# function that always returns 1 for now, lets not deal with foreign keys
# needs to be function as its called and not assigned
# TODO: fix this, satisfy unique contrstraint? check constraint
foreign_key = partial(next, count(1))
	


clear_screen = partial(subprocess.call, 'clear')
@click.command()
@click.option('--conf', type=click.Path(exists=True, dir_okay=False, file_okay=True), help='configuration file')
@click.option('--data', type=click.Path(exists=True, dir_okay=False, file_okay=True), help='initial data csv file to inject')
@click.option('--debug/--no-debug', type=bool, default=False)
@click.argument('directory', type=click.Path(exists=True,  file_okay=False, resolve_path=True))
@click.pass_context
def main(context, conf, data, debug, directory):
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
	# load initial data
	initial_data = None
	if data:
		csvfile = open(data, newline='', encoding='utf-8-sig')
		reader = csv.DictReader(csvfile, delimiter=',')
		initial_data = list(reader)
		csvfile.close()
	tables = context.obj.django.tables



	with TarotDatabaseConnection(context.obj.database) as tarot_db:
		#: selected / working table
		table = tables[0]
		click.echo(f'WARNING: droping table {table}')
		tarot_db.cursor.execute(f'DELETE FROM {table}')
		# build list of fields containing null values
		columns = {table: tarot_db.columns(table) for table in tables}
		if initial_data and columns[table] == initial_data[0].keys():
			initial_columns = set(initial_data[0].keys())
			columns_set = set(columns[table])
			null_fields = list(columns_set - initial_columns)
		else:
			null_fields = columns
		
		#: fake_map: maps which fake generator to use for each field
		fakes = dict()
		types = dict(word=word, paragraph=paragraph,
					bullets=bullets, number=number, thumbnail=thumbnail, foreign_key=foreign_key, boolean=boolean)
		pragma = None
		if table in context.obj.data_pragma:
			# we know the fake data types
			pragma = context.obj.data_pragma.get(table)
			for field in columns[table]:
				if field in pragma.keys():
					fake_type = pragma[field].get('type')
					fakes[field] = partial(types[fake_type])
				elif '_id' in field:
					# we dont support foreign_keys or other types of keys as of yet
					fakes[field] = types['foreign_key']
		else:
			# we don't know anything about what fake type to use, unknown model
			#: click choice , list of fake types to choose from
			type_choices = click.Choice(types.keys(), case_sensitive=False)
			# ask user what fake data to use for each null field / column
			for field in null_fields[table]:
				if (not 'id' in field and field.lower() != 'foreignkey'):
					fake_type = click.prompt(
						f'Type for {field}', type=type_choices, show_choices=True)
					fakes[field] = partial(types[fake_type])

		#: list of tuples (field.name, field.value)
		record_values = list()
		#: new_fields: fields that are defined in the model that dont exist in database table
		new_fields = find_new_fields(table)
		# read in the ddl
		try:
			with Path('./ddl.toml').open() as ddl_file:
				ddl = toml.load(ddl_file)
		except:
			click.echo(
				'DDL is missing, cannot add new columns... continuing without')
		# add new columns :: manual migration
		if ddl:
			engine = context.obj.database['ENGINE'].split('.')[-1]
			for field in new_fields:
				if field.fieldtype == "ForeignKey":
					click.echo(f'ForeignKey {field.name} found, unsupported, ignoring...')
					continue
				else:
					click.echo(f'Found {field.name}, adding...')
				sql_type = ddl[field.fieldtype][engine]
				tarot_db.cursor.execute(
					f'ALTER TABLE {table} ADD COLUMN {field.name} {sql_type}')
		placeholder_char = '%s' if 'postgresql' in tarot_db.database['ENGINE'] else '?'
		value_placeholder = ', '.join(
				placeholder_char for _ in range(1, len(columns[table]) + 1))
		if initial_data:
			num_records = len(initial_data)
		else:
			# no initial data, how many do we want
			num_records = click.prompt('How many records to add?', default = 1, type = int, show_default = True)
		record = dict()
		index = 0
		while(index < num_records):
			values = list()
			if initial_data:
				record = initial_data[index]
			for column in columns[table]:
				if column == 'id':
					value = foreign_key()
					values.append(value)
					continue
				if column in record.keys():
					values.append(record[column])
				elif '_id' in column:
					# set foreign_keys to None , only works if django field option null=True
					values.append(None)
					continue
				else:
					if pragma and pragma[column].get('type') == 'thumbnail':
						value = fakes[column](index)
					else:
						value = fakes[column]()
					values.append(value)
			tarot_db.cursor.execute(
				f'INSERT INTO {table} ({", ".join(columns[table])}) VALUES({value_placeholder})', tuple(values))
			index += 1
		tarot_db.connection.commit()


if __name__ == "__main__":
	main(obj={})
