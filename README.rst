Flask Website
=============

The main website for https://archwomen.org

Installation
------------

Install python, flask, feedparser, pygments, markdown, dateutil and icalendar

Run
---

gunicorn service file is used to run the flask website but you can run a local
test with `python -m flask run`

Add Pages
---------

Pages are written in markdown and saved in `/content/pages` with the .md file
extension.

Todo
----

* events with ical on the main page [DONE]
* twitter feed? [DONE]
* blog
* blog archives
* cache with frozen flask
* contact form
