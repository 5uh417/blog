AUTHOR = 'Suhail'
SITENAME = "Suhail's Blog"
SITEURL = ""

PATH = "content"

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

# Menu items
MENUITEMS = (
    ('About', '/pages/about/'),
    ('Tags', '/tags/'),
    ('Archives', '/archives/'),
)

DEFAULT_PAGINATION = 10

THEME = 'themes/terminal-pelican'

# Clean URL structure
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Pages structure  
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

# Clean pagination
PAGINATED_URL = 'page/{number}/'
PAGINATED_SAVE_AS = 'page/{number}/index.html'

# Author pages
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'

# Category pages
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

# Archives
ARCHIVES_SAVE_AS = 'archives/index.html'

# Tags - disable individual tag pages, keep only tags listing
TAG_SAVE_AS = ''
TAGS_SAVE_AS = 'tags/index.html'

# Categories listing
CATEGORIES_SAVE_AS = 'categories/index.html'

# Authors listing
AUTHORS_SAVE_AS = 'authors/index.html'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
