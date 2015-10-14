#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# General Settings
AUTHOR = u'admin'
TIMEZONE = 'UTC'
DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

DATE_FORMATS = {
    'en': '%d %B %Y',
}

DEFAULT_PAGINATION = 20
RELATIVE_URLS = True
SITENAME = ('Ryan Liao Blog')
SITEURL = '.'
THEME = 'pirsquare'
THEME_STATIC_DIR = ('')

# Configuration to make sure blog is in sub directory and pages
# is in main directory
ARTICLE_PATHS = ['blog']
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'

PATH_PATHS = ['pages']
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{template}/{slug}.html'

DIRECT_TEMPLATES = (('index', ))
PAGINATED_DIRECT_TEMPLATES = (('index',))

# Other settings
PUBLISH = False

# Remove Unnecessary Stuffs
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

AUTHOR_SAVE_AS = (False)
AUTHORS_SAVE_AS = (False)
ARTICLE_LANG_SAVE_AS = (False)
CATEGORY_SAVE_AS = (False)
TAG_SAVE_AS = None


EMAIL = 'pirsquare.ryan@gmail.com'
GITHUB_URL = 'http://github.com/pirsquare'
BEHANCE_URL = 'http://behance.net/pirsquare'
RESUME_URL = 'http://pirsquare.io/resume/'
