import logging
logger = logging.getLogger('kisspy.' + __name__)

import datetime,time,random

import tornado.web
import momoko
from tornado import gen

from handlers.base import BaseHandler




from models import A,B,C

class AHandler(BaseHandler):
    '''Big Category Detail'''
    def get(self, aid):
        try:
            a = A.select().where(A.id==aid).get()
            chapters = [ (b,C.select().where(C.parent==b)) for b in B.select().where(B.parent==a)]
            context={'a':a, 'blist':chapters}
            books = A.select().order_by(A.id)
            context.update(books=books)
            self.render("index.html",**context)
        except A.DoesNotExist:
            raise tornado.web.HTTPError(404)

class BHandler(BaseHandler):
    '''Category List'''
    def get(self, aid, bid):
        b = B.select().where(B.id==bid).get()
        if b.parent.id != int(aid):
            aid = b.parent.id
            self.redirect('/%s_%s/' % (b.parent.id, bid))
        a = A.select().where(A.id==aid).get()
        chapters = [(b,C.select().where(C.parent==b))]
        context={'book':a,'chapter':b, 'chapters':chapters}
        books = A.select().order_by(A.id)
        context.update(books=books)
        self.render("index.html",**context)

class CHandler(BaseHandler):
    '''Smallest Item Detail'''
    def get(self, aid, bid, cid):
        try:
            b = B.select().where(B.id==bid).get()
        except B.DoesNotExist:
            raise tornado.web.HTTPError(404)

        b = B.select().where(B.id==bid).get()
        if b.parent.id != int(aid):
            aid = b.parent.id
            self.redirect('/%s_%s/%s.html' % (b.parent.id, bid, cid))

        a = A.select().where(A.id==aid).get()

        try:
            c = C.select().where(C.id==cid).get()
        except C.DoesNotExist:
            raise tornado.web.HTTPError(404)
        try:
            nextone  = C.select().where(C.id>c.id, C.parent==b).order_by(C.id).get()
        except C.DoesNotExist:
            nextone = None
        try:
            previous = C.select().where(C.id<c.id, C.parent==b).order_by(C.id.desc()).get()
        except C.DoesNotExist:
            previous = None


        context={'book':a,'chapter':b,'article':c,'previous':previous,'next':nextone}
        books = A.select().order_by(A.id)
        context.update(books=books)
        print context
        self.render("detail.html",**context)

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

class UploadFileHandler(BaseHandler):
    def get(self):
        self.render("upload-file.html")

    def post(self):
        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open("/data/web/upload/%s" % filename, "wb")
            f.write(file_dict["body"])
            f.close()
        self.write("finish")
