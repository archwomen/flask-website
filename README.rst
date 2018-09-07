Flask Website
=============

The main website for https://archwomen.org

Installation
------------

Install python, flask, feedparser, pygments, markdown, dateutil, icalendar
bleach

Pip command:

    pip install flask feedparser pygments markdown dateutil icalendar bleach

pacman:

    pacman -S python-flask python-feedparser python-pygments python-markdown python-dateutil python-icalendar python-bleach

Run
---

On the server gunicorn service file is used to run the flask website but you can run a local
test with `export FLASK_APP=app.py; export DEV=yes; python -m flask run` then go to
`localhost.localdomain:5000` to see the website.

To allow sessions on production a secret key enviromental variable should be set
in the systemd service file running the site.

On the server this enviromental variable is set by doing the following:

    systemctl edit gunicorn.service

Then you need to edit the file and add:

    Environment="SECRET_KEY=mysupersecretekey"

Obviously with a different key. This key is used for storing the contact form
capcha to validate it. Note that sessions should NOT be used for any information 
you actually need to keep secure.

Add Pages
---------

Pages are written in markdown and saved in `/content/pages` with the .md file
extension.

Todo
----

* blog
* blog archives
* cache with frozen flask
