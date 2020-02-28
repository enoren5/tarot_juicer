"""
WARNING: This script will DELETE all records of the spesified table before injections

This script uses source data from previously generated csv file as well as a images folder
provided via command line arguments, to first DELETE all records of specified table before
INSERT new records obtained from the aforementioned csv, it proceeds to inject binary
image data from each image of the images folder into the spesified database,table,field
as per command line arguments
    database: 'name of database file'
    media_url: 'the location django expects the images to be'
    images 'folder containing images to be injected'
"""
import sqlite3
import pandas
import argparse
import tempfile
import numpy
from pathlib import Path
from shutil import copyfile
from faker import Faker
from faker.providers import lorem
from functools import partial

fake = Faker()  # generates fake data includes lorem
fake.add_provider(lorem)

""" Lorem ipsum words, the more the better """
LOREM = ("Phasellus vitae fringilla lectus, sed laoreet dui. Aliquam facilisis lacus justo, eu fringilla lacus mollis vitae. Sed eget lorem egestas, malesuada magna ut, mattis felis.".split())

""" Context for handling connection to database """
class TarotDatabaseConnection(object):
    def __init__(self, database):
        self.connection = None
        self.cursor = None
        self.database = database

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *exc):
        self.connection.close()

""" generates string representing bullets where each bullet is delimited by a newline
    and user spesifies desired number of bullets, and how many words each bullet should contain """
def bullets(num_bullets, words_per):
    return "\n".join(
        fake.sentence(nb_words=words_per, ext_word_list=LOREM, variable_nb_words=False)
        for _ in range(num_bullets)
    )

""" generator functions for creating desired ammount of lorem ipsum """
bullet = partial(bullets, 6, 3)
word = partial(fake.word, ext_word_list=LOREM)
paragraph = partial(fake.paragraph, ext_word_list=LOREM, nb_sentences=6, variable_nb_sentences=True)


if __name__ == "__main__":
    # pandas was being anal about relative paths
    CSV_SRC = (Path(__file__).parent / Path('./data.csv')).resolve().as_posix()
    THUMBNAILS = ('thumbnails')
    TABLE_NAME = ('generators_generator')
    FIELD = ('tarot_card_thumbnail')
    GLOB = (r'*.jpg')

    parser = argparse.ArgumentParser(
        description="Script to inject images into sqlite3 database field, in additon to csv data"
    )
    parser.add_argument("database", help="sqlite3 database file")
    parser.add_argument("media_dir", help="the location django expects the images to be")
    parser.add_argument("images_dir", help="folder containing images")

    arguments = parser.parse_args()
    database = arguments.database
    image_dir = Path(arguments.images_dir)
    media_dir = Path(arguments.media_dir, THUMBNAILS)
    fields = ("id,title,number,tarot_card_image,astrological,alchemical,"
                "intelligence,hebrew_letter,letter_meaning,description,"
                "galileo_content,f_loss_content,st_paul_content,f_loss_bullets,"
                "galileo_bullets,st_paul_bullets,description_bullets,"
                "slashdot_position,watchtower_position,tarot_card_thumbnail").strip().split(",")
    field_types = {
        "title": numpy.object,
        "number": numpy.int64,
        "tarot_card_image": numpy.object,
        "astrological": numpy.object,
        "description": numpy.object,
    }
    lorem_generators = {
            "alchemical": word,
            "intelligence": word,
            "hebrew_letter": word,
            "letter_meaning": word,
            "galileo_content": paragraph,
            "f_loss_content": paragraph,
            "st_paul_content": paragraph,
            "description_bullets": bullet,
            "galileo_bullets": bullet,
            "f_loss_bullets": bullet,
            "st_paul_bullets": bullet
    }

    csv_data = pandas.read_csv(CSV_SRC, dtype=field_types, keep_default_na=True)

    with TarotDatabaseConnection(database) as db:
        # copy thumbnails
        image_fnames = sorted([img.name for img in image_dir.glob(GLOB)], key=lambda x: x.lstrip('K'))
        for image in image_fnames:
            copyfile(image_dir / image, media_dir / image)

        """ drop existing records from table, insert data """
        db.cursor.execute(f"DELETE FROM {TABLE_NAME}")
        columns = db.cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        if FIELD not in [desc[0] for desc in db.cursor.description]:
            # add if missing tarot_card_thumbnail field
            db.cursor.execute(f'ALTER TABLE {TABLE_NAME} ADD {FIELD} VARCHAR (1024)')
            db.connection.commit()

        # gather data
        for record in csv_data.itertuples(index=False):
            # get url to image, due to origional file naming 0 is treated without 0 postfix
            image_file = f"{THUMBNAILS}/{image_fnames[record.number]}"
            """ generators_generator : 
            id, title, number, tarot_card_image, astrological, alchemical, intelligence, hebrew_letter, letter_meaning, description, galileo_content, f_loss_content, st_paul_content, f_loss_bullets, st_paul_bullets, description_bullets, slashdot_position, watchtower_position, tarot_card_thumbnail """


            """ construct missing fields, from lorem generators """
            data = dict()
            for field in fields:
                if (field in lorem_generators):
                    value = lorem_generators.get(field)()
                elif (field == FIELD):
                    value = image_file
                elif (field in csv_data.columns):
                    value = getattr(record, field)
                else:
                    value = None
                data[field] = value
            
            data_values = tuple(value for value in data.values())
            placeholders = ('?,' * len(data)).rstrip(',')
            sql = f"INSERT INTO {TABLE_NAME} {tuple(fields)} VALUES ({placeholders})"
            db.cursor.execute(sql, data_values)
            
        db.connection.commit()
