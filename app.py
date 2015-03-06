# Python imports
import os

# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import psycopg2

from tornado.options import define, options

# App imports
import forms
import uimodules

from utils.importlib import import_module

import logging
# the root logger is created upon the first import of the logging module

# create a file handler to add to the root logger
filehandler = logging.FileHandler(
    filename = 'test.log',
    mode = 'a',
    encoding = None,
    delay = False
)

# set the file handler's level to your desired logging level, e.g. INFO
filehandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s %(lineno)d]: %(levelname)s: %(message)s')
filehandler.setFormatter(formatter)

# set the root logger's level to be at most as high as your handler's
#if logging.root.level > filehandler.level:
#    logging.root.setLevel = filehandler.level

# finally, add the handler to the root. after you do this, the root logger will write
# records to file.
logging.root.addHandler(filehandler)
logger = logging.getLogger('kisspy')
logger.addHandler(filehandler)

import settings
from urls import url_patterns

# Options
define("port", default=9000, help="run on the given port", type=int)
define("db_path", default='postgresql://huyoo:xyz2014@localhost:5432/cccc', type=str)

from models import db, Config

class Application(tornado.web.Application):
    def __init__(self):
        handlers = url_patterns

        tornado.web.Application.__init__(self, handlers, **settings.settings)
        self.timezone = 'Asia/Shanghai'
        self.db = db
        self.session_manager = self.create_session_manager()
        self.reload_config()

    def reload_config(self):
        try:
            config=Config.select().where(Config.id==1).get()
        except:
            config=Config(sitename='ABCcms', siteurl='http://localhost')
        config_keys=config._meta.fields.keys()
        print config_keys
        config_keys.remove('id')
        config_keys.remove('created_at')
        config_keys.remove('updated_at')
        for key in config_keys:
            if not hasattr(self,key):
                setattr(self,key,getattr(config, key))
            else:
                setattr(self,key,getattr(config, key))



    def create_session_manager(self):
        engine = import_module(settings.SESSION_ENGINE)
        return engine.SessionManager(settings.SESSION_SECRET, settings.MEMCACHED_ADDRESS, settings.SESSION_TIMEOUT)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
