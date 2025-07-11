AUTHOR = 'Suhail'
SITENAME = "~/dev/thoughts"
SITEURL = ""

PATH = "content"

# Content paths
ARTICLE_PATHS = ['posts']
PAGE_PATHS = ['pages']
STATIC_PATHS = ['static']

# Static files
# EXTRA_PATH_METADATA = {
#     'static/img': {'path': 'img'},
# }

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Social links
SOCIAL = (
    ("GitHub", "https://github.com/5uh417"),
    ("Twitter", "https://twitter.com/5uh417"),
    ("LinkedIn", "https://linkedin.com/in/suhailmirza"),
)

# Menu items - relative paths that work with SITEURL
MENUITEMS = (
    ('About', 'about/'),
    ('Tags', 'tags/'),
    ('Archive', 'archives/'),
)

DEFAULT_PAGINATION = 10

THEME = 'themes/terminal-pelican'

# Clean URL structure
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Pages structure - no "pages/" prefix
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Clean pagination - use simple numbers
PAGINATED_URL = '{number}/'
PAGINATED_SAVE_AS = '{number}/index.html'

# Author pages - no "author/" prefix
AUTHOR_URL = '{slug}/'
AUTHOR_SAVE_AS = '{slug}/index.html'

# Category pages - no "category/" prefix
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'

# Archives - simple name
ARCHIVES_SAVE_AS = 'archives/index.html'

# Tags - clean URL structure
TAG_URL = '{slug}/'
TAG_SAVE_AS = '{slug}/index.html'
TAGS_SAVE_AS = 'tags/index.html'

# Categories listing - simple name
CATEGORIES_SAVE_AS = 'categories/index.html'

# Authors listing - simple name
AUTHORS_SAVE_AS = 'authors/index.html'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
