import logging
logger = logging.getLogger('kisspy.' + __name__)

import datetime,time,random

import tornado.web
import momoko
from tornado import gen

from handlers.base import BaseHandler

class HelpHandler(BaseHandler):
    def get(self):
        context={}
        self.render("help.html",**context)

class DownloadHandler(BaseHandler):
    def get(self):
        context={}
        self.render("download.html",**context)

class ServiceHandler(BaseHandler):
    def get(self):
        context={}
        self.render("service.html",**context)

class FeaturesHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class ContactusHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class AboutusHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class PrivacyHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class FAQHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class LegalHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class DeclareHandler(BaseHandler):
    def get(self):
        context={}
        self.render("features.html",**context)

class WebsiteShutdownHandler(BaseHandler):
    def get(self):
        context={}
        self.render("shutdown.html",**context)
