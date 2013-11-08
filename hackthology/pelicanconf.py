#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Tim Henderson'
SITENAME = u'Hackthology'
SITEURL = ''
THEME = 'theme/'
TIMEZONE = 'US/NewYork'
DEFAULT_LANG = u'en'

GOOGLE_ANALYTICS = 'UA-20145944-2'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'footnotes']

#TEMPLATE_PAGES = {
  #'index.html': 'output/index.html'
#}

#STATIC_PATHS = [
    #'html/index.html',
#]
#EXTRA_PATH_METADATA = {
    #'html/index.html': {'path': 'index.html'},
#}
ARTICLE_EXCLUDES = ['pages','html']

DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives'))

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
          #('Python.org', 'http://python.org/'),
          #('Jinja2', 'http://jinja.pocoo.org/'),
          #('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github.com/timtadh', 'https://github.com/timtadh'),
          ('Google+', 'https://plus.google.com/109232399292705173597'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

