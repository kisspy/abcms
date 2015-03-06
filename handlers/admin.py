from handlers.base import BaseHandler
from tornado import gen
import momoko
import tornado.web

import logging
logger = logging.getLogger('kisspy.' + __name__)

MAX_ADMIN_UID=2

from models import A,B,C,User, Link, Visit, Config
from settings import MEDIA_ROOT
import os
import time

class BaseAdminMixin(object):
    #def prepare(self):
    #    pass

    @gen.coroutine
    def get_visits(self, uid=None, page_size=100, offset=0):
        params={'offset':offset,'limit':page_size}
        visits = Visit.select().paginate((offset % page_size)+1, page_size)

        if uid:
            params.update({'uid':uid})
            visits = (Visit.select(Visit, User.nickname)
                          .where(Visit.uid==uid)
                          .join(User)
                          .group_by(Visit)
                          .paginate((offset % page_size)+1, page_size))
        else:
            visits = (Visit.select(Visit, User.nickname)
                          .join(User)
                          .group_by(Visit)
                          .paginate((offset % page_size)+1, page_size))

        raise gen.Return(visits)

    @gen.coroutine
    def get_visits_total(self, uid=None):
        if uid:
            results_count=Visit.select().where(Visit.uid==uid).count()
        else:
            results_count=Visit.select().count()
        raise gen.Return(results_count)

    @gen.coroutine
    def check_superuser(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')

class AdminHandler(BaseAdminMixin, BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        users_total=User.select().count()
        msg=None

        kwargs={
            'msg':msg,
            'users_total':users_total,
        }
        self.render("admin/index.html",**kwargs)

class AdminSystemHandler(BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        users_total=yield self.get_users_total()


        users=User.select()

        try:
            config=Config.select().where(Config.id==1).get()
        except Config.DoesNotExist:
            config=Config()


        msg=self.get_argument('msg','')
        page = int(self.get_argument('page','1'))
        page_size = 100
        offset = page_size*(page-1)




        kwargs={
            'msg':msg,
            'users':users,
            'users_total':users_total,
            'config':config,
        }
        self.render("admin/system.html",**kwargs)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        #print self.request
        #print self.request.body
        #print self.request.arguments
        #print self.request.files.keys()
        #print self.request.files['logo']
        #print '-'*80

        config_id = int(self.get_argument('config_id','1'))
        ip = self.get_argument('ip','')
        domain = self.get_argument('domain','')
        sitename = self.get_argument('sitename','')
        siteurl = self.get_argument('siteurl','')
        title  = self.get_argument('title','')
        keywords = self.get_argument('keywords','')
        description = self.get_argument('description','')
        copyright = self.get_argument('copyright','')
        shutdown = int(self.get_argument('shutdown','0'))
        reason = self.get_argument('reason','')
        logo = self.get_argument('logo','')
        print logo

        try:

            file_dict_list = self.request.files['logo']
        except KeyError:
            filename = None # no image uploaded
        else:
            for fd in file_dict_list:
                filename = fd["filename"]
                ext=filename.split('.')[-1]
                filename = 'logo%s.%s' % (str(int(1000*(time.time()))), ext)
                filepath = os.path.join(MEDIA_ROOT, 'images', filename)
                f = open(filepath, "wb")
                f.write(fd["body"])
                f.close()


        try:
            config=Config.select().where(Config.id==config_id).get()
        except:
            config_count= Config.select().count()
            if config_count>0:
                raise tornado.web.HTTPError(500, 'Server Config is broken!')
            else:
                defaults={}
                config=Config(sitename='ABCcms', siteurl='http://localhost')
                config.save()
        print config
        print 'shutdown', bool(shutdown)
        config.sitename=sitename
        config.siteurl=siteurl
        config.title=title
        config.keywords=keywords
        config.description=description
        config.copyright=copyright
        config.shutdown=bool(shutdown)
        config.reason=reason
        config.ip=ip
        config.domain=domain
        if filename:
            config.logo=filename
        config.save()

        self.application.reload_config()

        self.redirect('/admin/system')


class AdminThreadHandler(BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        users_total=yield self.get_users_total()

        users=User.select()


        msg=self.get_argument('msg','')
        page = int(self.get_argument('page','1'))
        page_size = 100
        offset = page_size*(page-1)




        kwargs={
            'msg':msg,
            'users':users,
            'users_total':users_total,
        }
        self.render("admin/thread.html",**kwargs)

class AdminUserHandler(BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        users_total=yield self.get_users_total()

        users=User.select()


        msg=self.get_argument('msg','')
        page = int(self.get_argument('page','1'))
        page_size = 100
        offset = page_size*(page-1)

        kwargs={
            'msg':msg,
            'users':users,
            'users_total':users_total,
        }
        self.render("admin/user.html",**kwargs)


class AdminVisitHandler(BaseAdminMixin, BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')

        users_total=yield self.get_users_total()

        users=User.select()

        msg=self.get_argument('msg','')
        page = int(self.get_argument('page','1'))
        page_size = 100
        offset = page_size*(page-1)

        results_count=yield self.get_visits_total()
        visits=yield self.get_visits(offset=offset)



        kwargs={
            'msg':msg,
            'users':users,
            'users_total':users_total,
            'visits':visits,
            'results_count':results_count,
            'page_size':page_size,
            'page':page
        }

        self.render("admin/visit.html",**kwargs)

class AdminLoginHandler(BaseAdminMixin, BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        kwargs={
        }

        self.render("admin/login.html",**kwargs)

class AdminLogoutHandler(BaseAdminMixin, BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        self.clear_cookie(self.djbhash('user'))
        self.redirect('/')

class AdminChannelHandler(BaseHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        #print repr(self.application.sitename)
        user=self.get_current_user()
        if user:
            logger.error(str(user))
            if user['uid']>MAX_ADMIN_UID:
                raise tornado.web.HTTPError(404,'Page Not Found!')
        users_total=yield self.get_users_total()


        users=User.select()

        channels=A.select()

        try:
            config=Config.select().where(Config.id==1).get()
        except Config.DoesNotExist:
            config=Config()


        msg=self.get_argument('msg','')
        page = int(self.get_argument('page','1'))
        page_size = 100
        offset = page_size*(page-1)




        kwargs={
            'msg':msg,
            'users':users,
            'channels': channels,
            'users_total':users_total,
            'config':config,
        }
        self.render("admin/channel.html",**kwargs)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        #print self.request
        #print self.request.body
        #print self.request.arguments
        #print self.request.files.keys()
        #print self.request.files['logo']
        #print '-'*80

        config_id = int(self.get_argument('config_id','1'))
        ip = self.get_argument('ip','')
        domain = self.get_argument('domain','')
        sitename = self.get_argument('sitename','')
        siteurl = self.get_argument('siteurl','')
        title  = self.get_argument('title','')
        keywords = self.get_argument('keywords','')
        description = self.get_argument('description','')
        copyright = self.get_argument('copyright','')
        shutdown = int(self.get_argument('shutdown','0'))
        reason = self.get_argument('reason','')
        logo = self.get_argument('logo','')
        print logo

        try:

            file_dict_list = self.request.files['logo']
        except KeyError:
            filename = None # no image uploaded
        else:
            for fd in file_dict_list:
                filename = fd["filename"]
                ext=filename.split('.')[-1]
                filename = 'logo%s.%s' % (str(int(1000*(time.time()))), ext)
                filepath = os.path.join(MEDIA_ROOT, 'images', filename)
                f = open(filepath, "wb")
                f.write(fd["body"])
                f.close()


        try:
            config=Config.select().where(Config.id==config_id).get()
        except:
            config_count= Config.select().count()
            if config_count>0:
                raise tornado.web.HTTPError(500, 'Server Config is broken!')
            else:
                defaults={}
                config=Config(sitename='ABCcms', siteurl='http://localhost')
                config.save()
        print config
        print 'shutdown', bool(shutdown)
        config.sitename=sitename
        config.siteurl=siteurl
        config.title=title
        config.keywords=keywords
        config.description=description
        config.copyright=copyright
        config.shutdown=bool(shutdown)
        config.reason=reason
        config.ip=ip
        config.domain=domain
        if filename:
            config.logo=filename
        config.save()

        self.redirect('/admin/channel')
