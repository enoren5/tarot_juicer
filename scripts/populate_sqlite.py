"""
WARNING: This script will DELETE all records of the spesified table before injections

This script uses source data from previously generated csv file as well as a images folder
provided via command line arguments, to first DELETE all records of specified table before
INSERT new records obtained from the aforementioned csv, it proceeds to inject binary
image data from each image of the images folder into the spesified database,table,field
as per command line arguments
    database: 'name of database file'
    images 'folder containing images to be injected'
"""
import sqlite3
import pandas
import argparse
import tempfile
from pathlib import Path



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

def injectMissingField(database, table, field):
    with TarotDatabaseConnection(database) as db:
        #ALTER TABLE {tableName} ADD COLUMN COLNew {type};
        db.cursor.execute(f'ALTER TABLE {table} ADD {field} VARCHAR (1024)')
        db.connection.commit()


if __name__ == "__main__":
    CSV_SRC = 'data.csv'
    MEDIA_URL = 'thumbnails/'
    data = pandas.read_csv(CSV_SRC)
    parser = argparse.ArgumentParser(
        description="Script to inject images into sqlite3 database field, in additon to csv data"
    )
    parser.add_argument("database", help="sqlite3 database file")
    parser.add_argument("images", help="folder containing images")
    arguments = parser.parse_args()
    database = arguments.database
    table_name = arguments.table
    field = arguments.field
    image_dir = Path(arguments.images)
    fields = ("id,title,number,tarot_card_image,astrological,alchemical,"
                "intelligence,hebrew_letter,letter_meaning,description,"
                "galileo_content,f_loss_content,st_paul_content,f_loss_bullets,"
                "galileo_bullets,st_paul_bullets,description_bullets,"
                "slashdot_position,watchtower_position,tarot_card_thumbnail").strip().split(",")

    injectMissingField(database, table_name, field)

    with TarotDatabaseConnection(database) as db:
        # drop existing records from table
        db.cursor.execute(f"DELETE FROM {table_name}")
        db.connection.commit()


        for index, record in data.iterrows():
            if record['number'] != 0:
                image_file = f"{MEDIA_URL}K{record['number']:02d}.jpg"
            else:
                image_file = f"{MEDIA_URL}K{record['number']}.jpg"
            # image = list(image_dir.glob(image_file))[0]
            # image = imageToBinary(image)

            data_values = [record[field] for field in fields[:-1]]
            data_values.append(image_file)
            data_values = tuple(data_values)
            placeholders = ("?," * len(fields)).rstrip(',')
            sql = f"INSERT INTO {table_name} {tuple(fields)} VALUES ({placeholders})"
            db.cursor.execute(sql, data_values)
            db.connection.commit()

