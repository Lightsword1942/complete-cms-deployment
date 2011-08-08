# coding=utf-8
# Django settings for cms project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

CACHE_BACKEND = 'locmem:///'

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_URL = '/static/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

JQUERY_JS = 'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'
JQUERY_UI_JS = 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js'
JQUERY_UI_CSS = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/smoothness/jquery-ui.css'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*xq7m@)*f2awoj!spa0(jibsrz9%c0d=e(g)v*!17y(vx0ue_3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "staticfiles.context_processors.static",
    "django.core.context_processors.media",
    "sekizai.context_processors.sekizai",
    "cms.context_processors.media",
)

INTERNAL_IPS = ('127.0.0.1','89.151.221.9')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cmsplugin_blog.middleware.MultilingualBlogEntriesMiddleware',
    'cbv.middleware.DeferredRenderingMiddleware'
)

ROOT_URLCONF = 'cms_example.urls'

INSTALLED_APPS = (

    'cms_example',
    'postfixadmin',
    
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',

    'staticfiles',
    'mptt',
    'tinymce',
    'reversion',
    'sekizai',  

    'cms',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.twitter',
    'menus',

    'haystack',
    'cms_facetsearch',

    'djangocms_utils',
    'simple_translation',
    'cmsplugin_blog',
    'cmsplugin_blog_search',
    'tagging',
    
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'easy_thumbnails',

    'pagination',
    'south'
)

gettext = lambda s: s

LANGUAGE_CODE = "nb"

CMS_LANGUAGES = (
    ('nb', gettext('Norwegian Bokmal')),
    ('en', gettext('English')),
)

LANGUAGES = CMS_LANGUAGES

CMS_TEMPLATES = (
    ('cms_example/tpl_home.html', gettext('home')),
    ('cms_example/tpl_master.html', gettext('master')),
    ('cms_example/tpl_col-two.html', gettext('twocols')),
    ('cms_example/tpl_col-three.html', gettext('threecols'))

)

CMS_SOFTROOT = True
CMS_REDIRECTS = True

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    "height": "480",
    "plugins": "table,paste,searchreplace",
"theme_advanced_buttons1": "bold,italic,underline,strikethrough,|,sub,sup,|,charmap,|,formatselect,|,link,unlink,anchor,|,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,outdent,indent,blockquote",
"theme_advanced_buttons2": ",cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,cleanup,help,code,|,insertdate,inserttime",
"theme_advanced_buttons3": "tablecontrols,|,hr,removeformat,visualaid",
"theme_advanced_toolbar_location": "top",
"theme_advanced_toolbar_align": "left",
"theme_advanced_statusbar_location": "bottom",
"theme_advanced_resizing": "true",
"extended_valid_elements" : "a[href|onclick|target|class]"
}   

DJANGOCMS_UTILS_SEARCH_FACET=True

FORCE_LOWERCASE_TAGS = True

CMSPLUGIN_BLOG_PLACEHOLDERS = ('excerpt','content')

from easy_thumbnails import defaults

THUMBNAIL_PROCESSORS = defaults.PROCESSORS + (
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
)
THUMBNAIL_DEBUG = DEBUG

HAYSTACK_SEARCH_ENGINE= 'solr'
HAYSTACK_SITECONF = 'cms_example.search_sites'

try:
    from local_settings import *
except ImportError:
    pass

import djcelery
djcelery.setup_loader()