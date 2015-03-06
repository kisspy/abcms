import os
import tornado.template
from tornado.options import define, options

import uimodules

DEBUG=True

# Options
define("debug", default=True, type=bool)

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = path(ROOT, 'media')
STATIC_ROOT = path(ROOT, 'themes','douluodalu')
TEMPLATE_ROOT = path(STATIC_ROOT,'templates')

SESSION_ENGINE='sessions.backends.memcached'
SESSION_COOKIE_NAME='sessionid'
SESSION_SECRET='3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc'
SESSION_TIMEOUT = 60  # 60 secends
MEMCACHED_ADDRESS=["127.0.0.1:11211"]


SITENAME='NUMBERS.GLOBAL'

settings = dict(
  debug=options.debug,
  autoescape=None,
  static_path=STATIC_ROOT,
  template_path=TEMPLATE_ROOT,
  #template_loader=tornado.template.Loader(TEMPLATE_ROOT),
  xsrf_cookies=True,
  cookie_secret='ZTQ1YmY4NjdiMzRkM2NjYmI0ZjhmNWZmY2Y5NjQzZTUwNzJmZmQzNzhlMzA3NDYy',
  ui_modules=uimodules,
  static_url_prefix="/themes/",
  login_url="/user/login",
  SITENAME='NUMBERS.GLOBAL',
)

if settings['debug']:
    import mimetypes
    mimetypes.add_type("image/png", ".png", True)
