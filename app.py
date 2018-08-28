#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
archwomen.org website
"""

import os
import codecs
import re
import feedparser
import icalendar
from datetime import datetime, timedelta, tzinfo
from dateutil.rrule import *
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, abort, safe_join, request, flash
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from bleach.sanitizer import Cleaner
#from flask_frozen import Freezer

ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

def parse_recurrences(recur_rule, start, exclusions):
    """ Find all reoccuring events """
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=start)
    rules.rrule(first_rule)
    if not isinstance(exclusions, list):
        exclusions = [exclusions]
        for xdate in exclusions:
            try:
                rules.exdate(xdate.dts[0].dt)
            except AttributeError:
                pass
    now = datetime.now(utc)
    this_year = now + timedelta(days=90)
    dates = []
    for rule in rules.between(now, this_year):
        dates.append(rule.strftime("%D %H:%M UTC "))
    return dates

def sanitize_html(text):
    cleaner = Cleaner(tags=['acronym', 'blockquote', 'br', 'table', 'th', 'tr', 'td', 'caption', 'colgroup', 'col', 'thead', 'tbody', 'tfoot'],
                      attributes={'acronym': ['title']},
                      strip=False,
                      strip_comments=True,
                      filters=None) 
    sanitized = cleaner.clean(text)
    return sanitized

app = Flask(__name__)

@app.template_filter('markdown')
def markdown_filter(text):
    """ Convert markdown to html """
    safe_text = sanitize_html(text)
    return Markup(markdown(safe_text, extensions=[CodeHiliteExtension(linenums=False, css_class='highlight'), ExtraExtension()]))

@app.route('/pygments.css')
def pygments_css():
    formatter = HtmlFormatter(style='monokai', nobackground=True)
    defs = formatter.get_style_defs('.highlight')
    return defs, 200, {'Content-Type': 'text/css'}

@app.route('/')
def index():
    with open('static/data/Archwomen.ics', 'rb') as f:
        icalfile = f.read()
    gcal = icalendar.Calendar.from_ical(icalfile)
    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            description = component.get('description')
            location = component.get('location')
            startdt = component.get('dtstart').dt
            enddt = component.get('dtend').dt
            exdate = component.get('exdate')
            if component.get('rrule'):
                reoccur = component.get('rrule').to_ical().decode('utf-8')
                for item in parse_recurrences(reoccur, startdt, exdate):
                    events.append("{0} {1}<br>{2} - {3}"
                                  .format(item, summary, description, location))
            else:
                events.append("{0}-{1} {2}<br>{3} - {4}"
                              .format(startdt.strftime("%D %H:%M UTC"),
                                      enddt.strftime("%D %H:%M UTC"),
                                      summary, description, location))
    calevents = sorted(events)
    feed = feedparser.parse('https://archwomen.org/blog/feed.atom').entries
    return render_template('index.html', entries=feed[0:6], calendar=calevents, title='Home')

@app.route('/donate/')
def donate():
    return render_template('donate.html', title="Donate", od=True)

#@app.route('/contact/', methods=['POST'])
#def contact():
#    msg = render_template("email.txt",
#                          name=form.name.data,
#                          email=form.email.data,
#                          subject=form.subject.data,
#                          message=form.message.data)
#    p = os.popen("/usr/bin/sendmail -f contact@archwomen.org -t -i", "w")
#    p.write(msg)
#    p.close()
#    return render_template('submit.html', title=submitted)

#@app.route('/blog/archives')

#@app.route('/blog/<int:year>/<int:month>/<int:day>')
#def daypage(year, month, day):
#    y, m, d = str(year), str(month), str(day)
#    postlist = "content/posts"
#    results = {}
#    for post in os.listdir(postlist):
#        if fnmatch.fnmatch(file, '{0}-{1}-{2}:*.md'.format(y, m, d)):
#            year, month, day, slug = re.split("^([0-9]{4})-([0-9]{2})-([0-9]{2}):([a-z]*).md", post, flags=re.IGNORECASE)[1:5]
#            results[file].append("/blog/{0}/{1}/{2}/{3}".format(year, month, day, slug))
#    if results:
#        return render_template('posts.html', links=results, title='blog - {0} {1}, {2}'.format(m, d, y))
#    else:
#        abort(404)

#@app.route('/blog/<int:year>/<int:month>/<int:day>/<slug>')
#def postpage(year, month, day, slug):
#    page = "content/posts/{0}-{1}-{2}:{3}.md".format(year, month, day, slug)
#    if os.path.isfile(page):
#        with codecs.open(page, encoding='utf-8', mode='r+') as f:
#            content = f.read()
#            return render_template('post.html', page_html=content, title="blog - " + slug)
#    else:
#        abort(404)

@app.route('/<path:webpage>/')
def page(webpage):
    page = 'content/pages/%s%s'%(webpage, '.md')
    if os.path.isfile(page):
        with codecs.open(page, encoding='utf-8', mode='r+') as f:
            content = f.read()
            return render_template('page.html', page_html=content, title=webpage)
    else:
        abort(404)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    #if len(sys.argv) > 1 and sys.argv[1] == "build":
    #    freezer.freeze()
    #else:
    #    app.run()
    app.run()
