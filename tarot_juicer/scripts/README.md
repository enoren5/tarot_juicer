## How to Use

Multiple smaller  automation scripts were consolidated into a single script file. 

If you have a database that needs the new card data use it like this:

`$ python scripts/populate_sqlite.py db.sqlite3 tarot_juicer/static/img scripts/thumbnails` where the first argument is the location of the database, second is the directory where to store the images, and last one points to a folder where you have the thumbnail (small) versions of the cards located. 

The script will create a directory `tarot_juicer/static/img/thumbnails` and put the files into that folder while updating the database. It also drops the whole table first so generators_generator table which belongs to the generator model gets purged of any current data when the script is done so also beware of that.

The script takes the db.sqlite3 database, drops the contents of the generators_generator table and populates it with data for each tarot card. It also reorders the cards such that the card number matches the id value, thus in sequential order

usage: $ populate_sqlite.py [-h] database media_dir images_dir

FYI:
```
Script to inject images into sqlite3 database field, in additon to csv data

positional arguments:
  database    sqlite3 database file
  media_dir   the location django expects the images to be
  images_dir  folder containing images

optional arguments:
  -h, --help  show this help message and exit
```