## About these scripts 
Regarding feature request (enhancement) described in [Issue #32](https://github.com/enoren5/tarot_juicer/issues/32), this new automation script inflates three different databases with lorem ipsum placeholder content:
1. local db.sqlite3 
2. local postges instance
3. remote postgres instance on Heroku

When the script is executed, it will drop the user selected database and proceed to inject lorem ipsum fake data, along with any supplied data.csv file (which is optional).

## Usage: 
```
$ injector.py [OPTIONS] DIRECTORY
 
 Options:
   --conf FILE           configuration file
   --data FILE           initial data csv file to inject
   --debug / --no-debug
   --help                Show this message and exit.
```

## Tutorial:
Here is one way of using the script:
`$ python injector.py --data data.csv ~/dev/projects/python/2018-and-2020/tarot_juicer`
The above must inside the `venv` with requirements built properly. This one-liner will only work inside the scripts/injector directory. If you run that command in any other location, it will not work.

Here is some sample expected output:
```
[django]
project: tarot_juicer
app: generators
model: Generator
database: {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/home/<user>/path/to/project/directory/tarot_juicer/db.sqlite3'}
directory: /home/<user>/path/to/project/directory/tarot_juicer
        
Accept this config? [Y/n]: y
WARNING: droping table generators_generator
ForeignKey content_changes_logged found, unsupported, ignoring...
ForeignKey biblio found, unsupported, ignoring...
```

## How to Use (deprecated)
~~Multiple smaller  automation scripts were consolidated into a single script file.~~

~~If you have a database that needs the new card data use it like this:~~

~~`$ python scripts/populate_sqlite.py db.sqlite3 tarot_juicer/static/img scripts/thumbnails` where the first argument is the location of the database, second is the directory where to store the images, and last one points to a folder where you have the thumbnail (small) versions of the cards located.~~

~~The script will create a directory `tarot_juicer/static/img/thumbnails` and put the files into that folder while updating the database. It also drops the whole table first so generators_generator table which belongs to the generator model gets purged of any current data when the script is done so also beware of that.~~

~~The script takes the db.sqlite3 database, drops the contents of the generators_generator table and populates it with data for each tarot card. It also reorders the cards such that the card number matches the id value, thus in sequential order~~

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

