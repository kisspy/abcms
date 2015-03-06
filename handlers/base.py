# Python imports
import os
import logging
logger = logging.getLogger('kisspy.' + __name__)

import hashlib
import time,datetime
import momoko

# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen

from peewee import fn
from models import User, Visit

import settings

from utils.importlib import import_module
import sessions

def DJBHash(s):
    '''Daniel J.Bernstein'''
    hash_n = 5381
    for x in s:
        hash_n = ((hash_n << 5) + hash_n) + ord(x)
    return str(hex(hash_n))

from functools import wraps
def trackvisitor(func):
    '''track every request on RequestHandler

    class SomeHandler(BaseHandler):
        @trackvisitor
        def get(self):
            pass

    '''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            key = self.request.headers['HTTP_X_KEY']
        except KeyError:
            key = None
        if key and key == os.environ.get('KEY'):
            #Process the request
            func(self, *args, **kwargs)
            return None
        #Redirect to Home Page
        return self.redirect('http://google.com', status=301)
    return wrapper

class Message(object):
    code=0
    message=''
    level='info' # debug, info, warn(alert), error

    def __init__(self, message, code=0, level='info'):
        self.message=message
        self.code=code
        self.level=level

class BaseUserMixin(object):

    def get_login_url(self):
        return u"/user/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie(self.djbhash('user'))
        if user_json:
            user = tornado.escape.json_decode(user_json)
            user['is_administrator']=self.session.get('is_administrator', False)
            user['is_loggedin']=self.session.get('is_loggedin', False)
            user['is_agent']=self.session.get('is_agent', 0) # is_agent is agent id
        else:
            #user=dict(nickname=None,uid=None,email=None,username=None)
            #user['is_administrator']=self.session.get('is_administrator', False)
            #user['is_loggedin']=self.session.get('is_loggedin', False)
            user=None
        return user

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie(self.djbhash('user'), tornado.escape.json_encode(user), expires_days=None)
        else:
            self.clear_cookie(self.djbhash('user'))

    def djbhash(self, s):
        if settings.DEBUG:
            return s
        else:
            return DJBHash(s)

    def encrypt(self, password):
        return hashlib.sha1(password).hexdigest()

    @gen.coroutine
    def exist(self, username=None, email=None):
        result = False

        msg='''{result:'false'}'''

        if email or username:
            if not email:
                email=self.encrypt(username)

            try:
                user=User.select().where(User.username==username | User.email==email).get()
            except:
                user=None
        else:
            user=None

        if user:
            result=True
            user={'uid':user.id}
        else:
            user=None
        raise gen.Return((result,user))

    @gen.coroutine
    def authenticate(self, username=None, email=None, password=None):
        user = None
        print 'email',email
        print 'username',username
        print '1password',password
        msg='''{result:'false'}'''
        if password:
            password = self.encrypt(password)
            if email:
                query=User.select().where(User.email==email, User.password==password)
            elif username:
                query=User.select().where(User.username==username, User.password==password)

            try:
                record=query.get()
            except User.DoesNotExist:
                record=None

            if record:
                user={'uid':record.id,'email':record.email,'username':record.username,'nickname':record.nickname,'retcode':0}
                msg='''{result:'true',uid:%s}''' % record.id
            else:
                msg='''{result:'false', msg:'password is incorrect'}'''
        else:
            msg='''{result:'false', msg:'password is empty'}'''
        raise gen.Return((user,msg))

    @gen.coroutine
    def add_user(self, **kwargs):
        email = kwargs.get('email','')
        username = kwargs.get('username','')
        raw_password = kwargs.get('password','')
        nickname = kwargs.get('nickname','')
        is_active = kwargs.get('is_active',True)

        #print 'password',raw_password
        password = self.encrypt(raw_password)
        #print 'password',password
        kwargs.update(password=password)

        if not email:
            email=self.encrypt(username)
        kwargs.update(email=email)

        exist, user = yield self.exist(email=email, username=username)
        if exist:
            user.update(email=email, username=username)
            raise gen.Return(user)

        record = User(email=email, username=username, password=password, nickname=nickname)
        record.save()

        if record is None:
            raise gen.Return(None)
        user={'uid':record.id,'email':record.email,'username':record.username,'nickname':record.nickname,'retcode':0}
        raise gen.Return(user)

    @gen.coroutine
    def get_user(self,uid=None):
        sql = '''select id, username, email, nickname
        from ksforum.forum_users
        where id=%(uid)s
        '''
        params={'uid':uid}
        cursor = yield momoko.Op(self.db.execute, sql, params)
        record = cursor.fetchone()
        raise gen.Return(record)

    @gen.coroutine
    def get_user_json(self, record):
        '''record is an user record with id, username, email, nickname attr'''
        if record is None:
            raise gen.Return(None)
        user={'uid':record.id,'email':record.email,'username':record.username,'nickname':record.nickname, 'retcode':0}
        raise gen.Return(user)

    @gen.coroutine
    def get_user_info(self, uid):
        user=User.select().where(User.id==uid).get()
        raise gen.Return(user)

    @gen.coroutine
    def get_users_total(self):
        #query=(User.select(fn.COUNT(User.id).alias('users_total')))
        query=User.select().count()
        raise gen.Return(query)


    @gen.coroutine
    def get_latest_user(self):
        sql ='select id, username, email, nickname from ksforum.forum_users order by id desc limit 1'
        params=None
        cursor = yield momoko.Op(self.db.execute, sql, params)
        record = cursor.fetchone()
        raise gen.Return(record)

    @gen.coroutine
    def track_user(self):
        user=self.get_current_user()
        remote_ip=self.request.remote_ip
        host = self.request.host

        user_agent = self.request.headers.get('User-Agent','')
        referer = self.request.headers.get('Referer','')
        x_forwarded_host=self.request.headers.get('X-Forwarded-Host','')
        x_forwarded_for=self.request.headers.get('X-Forwarded-For','')
        if x_forwarded_host and host.startswith('127.0.0.1'):
            name = referer.replace('http://'+x_forwarded_host,'')
        else:
            name = referer.replace('http://'+host,'')
        delta=1
        #logger.error(str(self.request))
        #                 /admin/visit|127.0.0.1:9000|127.0.0.1|www.qb.vc
        # name              /admin/visit
        # self.request.host 127.0.0.1:9000
        # remote_ip         127.0.0.1
        # x_forwarded_host  www.qb.vc

        logger.error('|'.join(['x_forwarded_for',x_forwarded_for]))
        #logger.error('|'.join([name,self.request.host,remote_ip,x_forwarded_host]))

        if x_forwarded_for:
            if x_forwarded_for.find(',') >-1:
                remote_ip=x_forwarded_for.split(',')[0]
            elif x_forwarded_for.find('|') >-1:
                remote_ip=x_forwarded_for.split('|')[0]
            else:
                remote_ip=x_forwarded_for

        stat = yield self.add_stats(name, delta)
        stat = yield self.add_track(name, host=remote_ip, ua=user_agent)

    @gen.coroutine
    def add_stats(self, name, delta=1, oid=0):
        user=self.get_current_user()
        if user:
            uid=user['uid']
        else:
            uid=0
        sql = '''select id from  ksforum.forum_stats
        where name=%(name)s and uid=%(uid)s
        limit 1
        '''
        params={'uid':uid,'name':name, 'delta':delta,'oid':oid}
        cursor = yield momoko.Op(self.db.execute, sql, params)
        record=cursor.fetchone()
        if record:
            sql = '''update ksforum.forum_stats
            set total=total+%(delta)s,
            updated_at=%(updated_at)s
            where name=%(name)s and oid=%(oid)s and uid=%(uid)s
            '''
            params={'uid':uid,'name':name, 'delta':delta,'oid':oid, 'updated_at':datetime.datetime.utcnow()}
            cursor = yield momoko.Op(self.db.execute, sql, params)
        else:
            sql = '''insert into ksforum.forum_stats
            (uid, name, oid, total)
            values(%(uid)s, %(name)s, %(oid)s, %(delta)s)
            '''
            params={'uid':uid, 'name':name, 'delta':delta,'oid':oid}
            cursor = yield momoko.Op(self.db.execute, sql, params)
        raise gen.Return(None)

    @gen.coroutine
    def add_track(self, path, host=None, ua=None):
        user=self.get_current_user()
        uid=0
        if user:
            uid=user['uid']

        hostid=0
        if host:
            sql = '''select id from  ksforum.forum_hosts
            where ip=%(ip)s
            limit 1
            '''
            params={'ip':host}
            cursor = yield momoko.Op(self.db.execute, sql, params)
            record=cursor.fetchone()
            if record:
                hostid=record.id
            else:
                sql = '''insert into ksforum.forum_hosts
                (id, ip) values(DEFAULT,%(ip)s)
                RETURNING id
                '''
                params={'ip':host}
                cursor = yield momoko.Op(self.db.execute, sql, params)
                record=cursor.fetchone()
                hostid=record.id
        uaid=0
        if ua:
            sql = '''select id from  ksforum.forum_useragents
            where agent=%(ua)s
            limit 1
            '''
            params={'ua':ua}
            cursor = yield momoko.Op(self.db.execute, sql, params)
            record=cursor.fetchone()
            if record:
                uaid=record.id
            else:
                sql = '''insert into ksforum.forum_useragents
                (id, agent) values(DEFAULT,%(agent)s)
                RETURNING id
                '''
                params={'agent':ua}
                cursor = yield momoko.Op(self.db.execute, sql, params)
                record=cursor.fetchone()
                uaid=record.id

        sql = '''insert into ksforum.forum_visits
        (uid, path, hostid, uaid)
        values(%(uid)s, %(path)s, %(hostid)s, %(uaid)s)
        '''
        params={'uid':uid, 'path':path, 'hostid':hostid,'uaid':uaid}
        cursor = yield momoko.Op(self.db.execute, sql, params)
        raise gen.Return(None)

class BaseHandler(BaseUserMixin, tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def sitename(self):
        return self.application.sitename

    @property
    def shutdown(self):
        return self.application.shutdown

    #@gen.coroutine
    def prepare(self):
        print 'request.uri', self.request.uri
        #invalid_request=False
        #fobidden_suffixes=['.php','.asp','.aspx','.jsp']
        #for suffix in fobidden_suffixes:
        #    if self.request.uri.endswith(suffix):
        #        invalid_request=True
        #        break
        #if invalid_request:
        #    raise tornado.web.HTTPError(404,'Page Not Found!')
        engine = import_module(settings.SESSION_ENGINE)
        self.session = engine.Session(self.application.session_manager, self)
        pass

        print '1'
        #super(BaseHandler, self).prepare()
        print '1->2'
        print self.request.arguments
        print self.request
        print 'self.shutdown',self.shutdown
        if self.shutdown:
            if not self.request.uri.startswith('/admin') or not self.request.uri.startswith('/shutdown')  :
                #raise tornado.web.HTTPError(500, 'Server is shutdown')
                self.redirect('/shutdown')
            else:
                pass
        else:
            pass

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace.update({'SITENAME':self.application.sitename})
        namespace.update({'SEO_TITLE':self.application.title})
        namespace.update({'SEO_KEYWORDS':self.application.keywords})
        namespace.update({'SEO_DESCRIPTION':self.application.description})
        if not namespace.has_key('message'):
            namespace['message']=None
        return namespace

class BaseSimpleHandler(BaseHandler):
    def prepare(self):
        print self.request.arguments
        if self.shutdown:
            raise tornado.web.HTTPError(500, 'Server is shutdown')
        else:
            pass