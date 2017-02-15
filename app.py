#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
archwomen.org website
"""

import os
import codecs
import feedparser
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, abort, safe_join, request, flash
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
#from flask_frozen import Freezer


app = Flask(__name__)

# For restructured text
#from docutils.core import publish_parts

#@app.template_filter('rst')
#def rst_filter(text):
#    return Markup(publish_parts(source=text, writer_name='html')['body'])

@app.template_filter('markdown')
def markdown_filter(text):
    """ Convert markdown to html """
    return Markup(markdown(text, extensions=[CodeHiliteExtension(linenums=False, css_class='highlight'), ExtraExtension()]))

@app.route('/pygments.css')
def pygments_css():
    formatter = HtmlFormatter(style='monokai', nobackground=True)
    defs = formatter.get_style_defs('.highlight')
    return defs, 200, {'Content-Type': 'text/css'}

@app.route('/')
def index():
    feed = feedparser.parse('https://archwomen.org/blog/feed.atom').entries
    return render_template('index.html', entries=feed[0:6], title='Home')

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
