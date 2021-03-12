# <p align="center"> TAROT JUICER</p>
<p align="center">:godmode:</p>
This is a rudimentary Django-based CMS which dynamically presents tarot-related content placed onto unconventional but familiar contexts such as hollywood film and historical biography. Our purpose is to overturn and reform the audience's perspective beyond all recognition. The author endeavours to reach out (or "appeal") to the broadest audience possible.

## DJANGO APPS

Here are Django apps I've created and what their purpose is:

- **generators**: When a web user clicks the 'random' button, it serves one of twenty two tarot keys arbitrarily. Each tarot card webpage includes:
   -  A picture of the tarot key
   -  The name of the key
   -  Astrological Attribute
   -  Alchemical Attribute
   -  Intelligence
   -  Hebrew Letter
   -  Letter Meaning
   -  Description of the symbolic meaning
   -  The description applied to:
      - Galileo
      - FLOSS
      - St Paul the Apostle
  
  This app houses the most dynamic functionality of my whole website
- **landings**: Serves the landing/home page (the `portal.html` template) showing the extraordinary 'global initiation' message. This app also serves the 'about' template which is a webpage which explains the basic who, what, when, why (or purpose) of the website in general (similar to the preface to a book)
- **essays**: Serves the `article.html` template which captures a curated list of the most high impact tarot cards and their application to Galileo and FLOSS (bound together simultaneously) along with a curated list of tart cards applied to St. Paul. This essays app also serves up static articles (without dynamic functionality) similar to a blog post - - for essays by the author on tarot applied to Forrest Gump and the war of ideas. This essays app even includes an 'objections' page for content involving anticipated rebuttals from my various audiences. This essays app also refers to a basic content_changelog.html template which enables the author to document changes made to essays or other content over time.
- **accounts**: This feature gives website visitors who land on the 'gateway' landing page to enter a passphrase to gain access the rest of the site.

## BUILD INSTRUCTIONS

For *nix:
```
$ virtualenv --python=python3.9 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

You will also need to install postgresql v12.3. On Manjaro/Arch, you may use this:
```
$ sudo pacman -S postgresql postgresql-libs
```
## USAGE NOTES
### Swapping lorem ipsum db out with real prod db content

The [official Heroku docs cover provisioning Postgres, designating a primary database, sharing Postgres db's between applications](https://devcenter.heroku.com/articles/heroku-postgresql), and more. This doc explains how to juggle/change/swap out one db instance for another.

### Handling db remote instances *but locally*

It's possible to run a remote AWS Postgres db *locally*. In the virtual environment, when running `(local env) $ python manage.py runserver`, it defaults to the local db.sqlite3. You should be able to see this in the runserver log in your shell. Another way to verify which config db variable is currently in use is using this: `(local env) $ echo $DATABASE_URL`. Next, exit the server and run: `(virtual env) $ export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/NAME'` (where the postgres address is copied directly from the config var in the Heroku project dashboard). Exit the local server again. Then run `(local env) $ unset DATABASE_URL`. If you run the server again locally with: `(local env) $ python manage.py runserver`, then that should restore the db.sqlite3 configuration. PLEASE NOTE: It's important that you handle all of the above commands in the same terminal emulator. If you run `export DATABASE_URL` in one terminal, and then have the server running in a different terminal, it won't work. Use all of the above commands in the same terminal.

### Config variables
In the Heroku Dashboard, here are some of the variables you need to change for it to work in the production enviornment:
* `DJANGO_DEBUG` : This config variable in production needs to be set to False to run the app, this will also resolve the check deploy issues
* `ALLOWED_HOSTS` : Set its value by adding multiple hosts as ( separating each host by a space) `host1 host2 host3`
* `ADMIN_PATH` : Set its value to make the admin path as secure as you prefer the best.

## PURPOSE

"In a world where men do battle over whose version of God is most accurate, I cannot adequately express the deep respect and admiration I feel toward an organization in which men of differing faiths are able to break bread together in a bond of comradery, brotherhood, and friendship," - - On Freemasonry courtesy of Dan Brown in a 2009 interview as quoted on page 48-49 in Mark E Koltko-Rivera's (2011) _Freemasonry: An Introduction_ (London England: Penguin Group)


