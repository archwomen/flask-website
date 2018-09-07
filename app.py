#!/usr/bin/env python2
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
archwomen.org website
"""

import os
import random
import codecs
import re
import feedparser
import icalendar
from datetime import datetime, timedelta, tzinfo
from dateutil.rrule import *
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, abort, safe_join, url_for, request, session
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.sane_lists import SaneListExtension
from markdown.extensions.smarty import SmartyExtension
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
    cleaner = Cleaner(tags=['a', 'abbr', 'b', 'blockquote', 'br', 'caption', 'code',
                            'col', 'colgroup', 'dd', 'del', 'div', 'dl', 'dt', 'em',
                            'figcaption', 'figure', 'h1', 'h2', 'h3', 'h4', 'h5',
                            'h6', 'hr', 'i', 'img', 'ins', 'li', 'mark', 'ol', 'p',
                            'pre', 's', 'span', 'strong', 'sub', 'sup', 'table',
                            'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'u', 'ul'],
                      attributes={'*': ['class', 'id'],
                                  'abbr': ['title'],
                                  'a': ['alt', 'href', 'title'],
                                  'img': ['alt', 'src', 'title']},
                      styles=[],
                      protocols=['http', 'https', 'mailto'],
                      strip=False,
                      strip_comments=True,
                      filters=None)
    sanitized = cleaner.clean(text)
    return sanitized

app = Flask(__name__)
app.config.from_object('app_settings')

@app.template_filter('markdown')
def markdown_filter(text):
    """ Convert markdown to html """
    md2html = markdown(text, extensions=[CodeHiliteExtension(linenums=False, css_class='highlight'),
                                          ExtraExtension(),
                                         SaneListExtension(),
                                         SmartyExtension(smart_dashes=True,
                                                          smart_quotes=False,
                                                         smart_angled_quotes=False,
                                                         smart_ellipses=False)])
    safe_html = sanitize_html(md2html)
    return Markup(safe_html)

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

@app.route('/contact/', methods=['GET'])
def contact():
    numbers = {1: '0N3', 2: '†wo', 3: 'ThГ33', 4: 'f0uГ', 5: 'f1v€', 6: '$|X', 7: 'S€\/EN', 8: 'e;gh+', 9: 'π1N3'}
    question = ""
    answer = ""
    for i in range(3):
        rannum = random.SystemRandom().randint(1, 9)
        question += '{0} '.format(numbers[rannum])
        answer += str(rannum)
    if 'goodanswer' in session:
        session.pop('goodanswer', None)
    session['goodanswer'] = answer
    return render_template('contact.html', title="Contact", captcha=unicode(question, 'utf-8'))

@app.route('/contact/', methods=['POST'])
def emailform():
    result = request.form
    user_answer = result['captcha']
    user_answer = ''.join(user_answer.split())
    if 'goodanswer' in session:
        correct_answer = session['goodanswer']
        session.pop('goodanswer', None)
    else:
        abort(403)
    if user_answer == correct_answer:
        msg = render_template("email.txt",
                               name=result['name'],
                              email=result['email'],
                              subject=result['subject'],
                              message=result['message'])
        try:
            p = os.popen("/usr/bin/sendmail -f contact@archwomen.org -t -i", "w")
            p.write(msg)
            p.close()
        except:
            return render_template('submit.html',
                                    title="Submit",
                                   status="There was an error and the email wasn't sent",
                                   message=result['message'])
        return render_template('submit.html',
                                title="Submit",
                               status="Email sent sucessfully. We will respond back soon.",
                               message=result['message'])
    else:
        return render_template('submit.html',
                                title="Submit",
                               status="The captcha was incorrect, please try again.",
                               message=result['message'])

@app.route('/sitemap/', methods=['GET'])
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    urls = []
    for root, dirs, files in os.walk("content/pages"):
        for file in files:
            if file.endswith(".md"):
                pagename = os.path.splitext(file)[0]
                urls.append("{0}{1}".format(url_for("index", _external=True), pagename))
    sitemap = render_template('sitemap.xml', pagelist=urls)
    return sitemap, 200, {'Content-Type': 'application/xml'}

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
