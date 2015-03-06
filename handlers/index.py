# Python imports
import os

# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web



# App imports
from handlers.base import BaseHandler

import forms

from models import A, B, C

class IndexHandler(BaseHandler):
    def get(self):
        form = forms.HelloForm()
        a=A.select().where(A.id==1).get()
        blist = [ (b,C.select().where(C.parent==b)) for b in B.select().where(B.parent==a)]
        context = {'a':a,'blist':blist,'form':form}
        alist = A.select().order_by(A.id)
        context.update(alist=alist)

        self.render('index.html', **context)

    def post(self):
        form = forms.HelloForm(self)
        if form.validate():
          self.write('Hello %s' % form.planet.data)
        else:
          self.render('index.html', form=form)


class BaseListHandler(BaseHandler):
    aid=1
    def get(self, aid=None):
        if aid is None:
            aid = self.aid
        form = forms.HelloForm()
        a=A.select().where(A.id==aid).get()
        blist = [(b,C.select().where(C.parent==b)) for b in B.select().where(B.parent==a)]
        context = {'a':a,'blist':blist,
            'form':form}

        self.render('index.html', **context)

class ManhuaHandler(BaseListHandler):
    aid=2

class TianhuodadaoHandler(BaseListHandler):
    aid=3

class XujiHandler(BaseListHandler):
    aid=4

class ZhoubianHandler(BaseListHandler):
    aid=5

class JueshitangmenHandler(BaseListHandler):
    aid=6

class JiushenHandler(BaseListHandler):
    def get(self):
        super(JiushenHandler, self).get(aid=7)

class QuanwenyueduHandler(BaseListHandler):
    aid=1
