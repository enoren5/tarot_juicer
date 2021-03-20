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

It's possible to run a remote AWS Postgres db *locally*. It's as straightforward as running:

`(local venv) $ export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/NAME'`
   
whose `DATABASE_URL` you can source from the Heroku Dashboard. If you are havinng trouble determining the right 'colored' DB you can use: 

`(local venv) $ heroku addons --app tarot-prod`

You can also use:

`(local venv) $ heroku pg:info --app tarot-prod`

These commands should reveal the name of the add-on to distinguish the db with 'lorem' content from the db with  'real' content.

It's also very important to note that when exporting a db locally, you need to do it inside the same terminal that the local dev server is running in. For this to work, you'll need to exit the currnet local dev server, unset the existing db, export the db, and then finally run the server again. 

You can view the current db configuration (probably db.sqlite3 default) with:

`(local venv) $ echo $DATABASE_URL`

**PLEASE NOTE** and to emphasize once more: It's important that you handle all of the above commands in the same terminal emulator. If you run `export $DATABASE_URL` in one terminal, and then have the server running in a different terminal, it won't work. Use all of the above commands in the same terminal that you are running the local server in.

### Config variables
In the Heroku Dashboard, here are some of the variables you need to change for it to work in the production enviornment:
* `DJANGO_DEBUG` : This config variable in production needs to be set to False to run the app, this will also resolve the check deploy issues
* `ALLOWED_HOSTS` : Set its value by adding multiple hosts as ( separating each host by a space) `host1 host2 host3`
* `ADMIN_PATH` : Set its value to make the admin path as secure as you prefer the best.
* `HEROKU_POSTGRESQL_<color>_URL` : `postgres://USER:PASSWORD@HOST:PORT/NAME` you can reset the `PASSWORD` variable _on the fly_ by using:
   ```
   (local venv) $ heroku pg:credentials:rotate
   ```
   If you compare the `postgres://USER:PASSWORD@HOST:PORT/NAME` in the Heroku dashboard before and after redunning the Heroku 'rotate' command, most of the variables remain the same however the USER and PASSWORD will be different. This protects keys that I may have previously referred to publiclly in the Issues section of this repo. More details can be gleaned from this Heroku help doc titled, [How do I make sure my Heroku Postgres database credentials are correct?](https://help.heroku.com/FE0S4CS4/how-do-i-make-sure-my-heroku-postgres-database-credentials-are-correct) which I found by Googling: 'how to update postgresql credentials in heroku'.

## PURPOSE

"In a world where men do battle over whose version of God is most accurate, I cannot adequately express the deep respect and admiration I feel toward an organization in which men of differing faiths are able to break bread together in a bond of comradery, brotherhood, and friendship," - - On Freemasonry courtesy of Dan Brown in a 2009 interview as quoted on page 48-49 in Mark E Koltko-Rivera's (2011) _Freemasonry: An Introduction_ (London England: Penguin Group)


