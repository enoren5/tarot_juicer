# <p align="center"> TAROT JUICER</p>

This is a rudimentary Django-based CMS which dynamically presents tarot-related content placed onto unconventional but familiar contexts such as hollywood film and historical biography. Our purpose is to overturn and reform the audience's perspective beyond all recognition. The author endeavours to reach out (or "appeal") to the broadest audience possible.

### DJANGO APPS

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

### BUILD INSTRUCTIONS

For *nix:
```
$ virtualenv --python=python3.8 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

You will also need to install postgresql v12.3. On Manjaro/Arch, you may use this:
```
$ sudo pacman -S postgresql postgresql-libs
```
### USAGE NOTE
- swapping lorem ipsum db out with real prod db content (heroku doc)
- running remote AWS Postgres db locally (first courtesty of John Elder, then Umar) 
  - In viritual environment, when you run the server with `$ python manage.py runserver`, it defaults to the local db.sqlite3. To refer to the remote AWS Postgres DB, run: `$ export FIRST_DB=postgres://USER:PASSWORD@HOST:PORT/NAME`. Exit the server. Then run `$ unset FIRST_DB`. Run the server again locally with: `$ python manage.py runserver`.
- changing credential manually on heroku from '0' to '1'

### PURPOSE

"In a world where men do battle over whose version of God is most accurate, I cannot adequately express the deep respect and admiration I feel toward an organization in which men of differing faiths are able to break bread together in a bond of comradery, brotherhood, and friendship," On Freemasonry courtesy of Dan Brown in a 2009 interview noted on page 48-49 in Mark E Koltko-Rivera's (2011) _Freemasonry: An Introduction_ (London England: Penguin Group)

<p align="center">:godmode:</p>
