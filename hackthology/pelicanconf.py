#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Tim Henderson'
SITENAME = u'Hackthology'
SITEURL = ''
THEME = 'theme/'
TIMEZONE = 'US/Eastern'
DEFAULT_LANG = u'en'

GOOGLE_ANALYTICS = 'UA-20145944-2'

PLUGIN_PATHS = ['../pelican-plugins/']
PLUGINS = ['sitemap']

SITEMAP = {
    'format': 'xml',
}

# Feed generation is usually not desired when developing
## (None, i.e. base URL is “/”)  The domain prepended to feed URLs.  Since feed
## URLs should always be absolute, it is highly recommended to define this (e.g.,
##    “http://feeds.example.com”). If you have already explicitly defined SITEURL
##   (see above) and want to use the same domain for your feeds, you can just set:
##  FEED_DOMAIN = SITEURL. 
FEED_DOMAIN = 'https://hackthology.com'
FEED_RSS = 'feeds/rss.xml'
#FEED_ALL_RSS = 'feeds/rss-all.xml'
#FEED_ATOM (None, i.e. no Atom feed)   Relative URL to output the Atom feed.
#FEED_RSS (None, i.e. no RSS)  Relative URL to output the RSS feed.
#FEED_ALL_ATOM ('feeds/all.atom.xml')  Relative URL to output the all posts Atom feed: this feed will contain all posts regardless of their language.
#FEED_ALL_RSS (None, i.e. no all RSS)  Relative URL to output the all posts RSS feed: this feed will contain all posts regardless of their language.
#CATEGORY_FEED_ATOM (‘feeds/%s.atom.xml’[2])   Where to put the category Atom feeds.
#CATEGORY_FEED_RSS (None, i.e. no RSS)   Where to put the category RSS feeds.
#TAG_FEED_ATOM (None, i.e. no tag feed)  Relative URL to output the tag Atom feed. It should be defined using a “%s” match in the tag name.
#TAG_FEED_RSS (None, ie no RSS tag feed)   Relative URL to output the tag RSS feed
#FEED_MAX_ITEMS  Maximum number of items allowed in a feed. Feed item quantity is unrestricted by default.

# MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'footnotes']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.footnotes': {},
    },
    'output_format': 'html5',
}

#TEMPLATE_PAGES = {
  #'index.html': 'output/index.html'
#}xxx

#STATIC_PATHS = [
    #'html/index.html',
#]
#EXTRA_PATH_METADATA = {
    #'html/index.html': {'path': 'index.html'},
#}
ARTICLE_EXCLUDES = ['pages','html']
STATIC_PATHS = ['images', 'pdfs', 'tars', '.well-known']
DIRECT_TEMPLATES = (('index', 'articles'))

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
          #('Python.org', 'http://python.org/'),
          #('Jinja2', 'http://jinja.pocoo.org/'),
          #('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/timtadh'),
    ('twitter', 'https://twitter.com/timtadh'),
    ('google+', 'https://plus.google.com/109232399292705173597'),
    ('keybase', 'https://keybase.io/tadh'),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

