## How to Use

From within this directory, run:
`$ python inject_sqlite.py ../db.sqlite3 generators_generator tarot_card_thumbnail ~/home/user/path/to/out`

Please note that: `out` as a directory  should already contain the thumbnail images named K0.jpg through K21.jpg. The script also requires a file to be present generators_generator.csv inside the folder where  the script is run from.

FYI:
```
usage: inject_sqlite.py [-h] database table field images

Script to inject images into sqlite3 database field, in additon to csv data

positional arguments:
  database    sqlite3 database file
  table       sqlite3 table name
  field       filed to inject the images
  images      folder containing images

optional arguments:
  -h, --help  show this help message and exit`
  
  ```
  Each script is depends on each other. So we may amalagamate them all into a single script in the future.
