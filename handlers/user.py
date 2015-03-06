import logging
logger = logging.getLogger('user.py')

import datetime, time, hashlib

import momoko
import tornado.web
from tornado import gen

from handlers.base import BaseHandler
from models import User, Visit
class LoginHandler(BaseHandler):

    def get(self):
        error = self.get_argument('error', '').strip()
        self.render('user/login.html',
            next=self.get_argument('next','/'),
            message=self.get_argument('error',''),
            error=error
        )

    @gen.coroutine
    def post(self):
        email = self.get_argument('email', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        next = self.get_argument('next', '')
        if not next:
            next='/user/home'

        # The authenticate method should match a username and password
        # to a username and password hash in the database users table.
        # Implementation left as an exercise for the reader.
        user,msg = yield self.authenticate(email=email, username=username, password=password)
        print msg

        if user:
            self.set_current_user(user)
            self.redirect(next)
        else:
            error_msg = tornado.escape.url_escape("Login Failed, username and password not match.")
            next = tornado.escape.url_escape(next)
            self.redirect("/user/login?next=%s&error=%s" % (next, error_msg))

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie('user')
        self.redirect('/')

class RegisterHandler(LoginHandler):

    def get(self):
        error = self.get_argument('error', '').strip()
        self.render('user/register.html',
            next=self.get_argument('next','/'),
            error=error,
        )

    @gen.coroutine
    def post(self):
        email = self.get_argument('email', '').strip()
        username = self.get_argument('username', '').strip()
        password1 = self.get_argument('password1', '').strip()
        password2 = self.get_argument('password2', '').strip()

        if password1 != password2:
            error_msg = tornado.escape.url_escape("Password is not match!")
            self.write(u'/user/register?error=' + error_msg)
            return

        if email == '':
            error_msg = tornado.escape.url_escape("Email is required!")
            self.redirect(u"/user/register?error=" + error_msg)
            return
        else:
            if email.find('@')==-1:
                error_msg = tornado.escape.url_escape("Email is invalid!")
                self.redirect(u"/user/register?error=" + error_msg)

        if not username:
            username=email.split('@')[0]

        exist,msg = yield self.exist(email=email, username=username)
        if exist:
            # exist user email or username
            error_msg = u'?error=' + tornado.escape.url_escape('Login name already taken')
            self.redirect(u'/user/register?error=' + error_msg)
            return

        if password1:
            password = password1
        else:
            error_msg = u'?error=' + tornado.escape.url_escape('Password not set')
            self.redirect(u'/user/register?error=' + error_msg)
            return

        user = {}
        user['email'] = email
        user['username'] = username
        user['password'] = password

        user = yield self.add_user(**user)
        if user:
            self.set_current_user(user)

        self.redirect('/user/home')
        return

class ForgotPasswordHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        error = self.get_argument('error', '').strip()
        self.render("user/forgotpassword.html",
            next=self.get_argument("next","/"),
            message=self.get_argument("error",''),
            error=error,
        )

    @gen.coroutine
    def post(self):
        email = self.get_argument('email', '')
        r = yield self.send_email(email=email, subject=subject, content=content)

        if r:
            self.redirect("/user/home")
        else:
            error_msg = tornado.escape.url_escape("Login Failed, username and password not match.")
            next = tornado.escape.url_escape('/userstats/')
            self.redirect("/user/login?next=%s&error=%s" % (next, error_msg))

class ModifyPasswordHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        error = self.get_argument('error', '').strip()
        self.render("user/modifypassword.html",
            next=self.get_argument("next","/"),
            message=self.get_argument("error",''),
            error=error,
        )

    @gen.coroutine
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        auth,msg = yield self.authenticate(username=username, password=password)

        if auth:
            self.set_current_user(username)
            self.redirect("/user/home")
        else:
            error_msg = tornado.escape.url_escape("Login Failed, username and password not match.")
            next = tornado.escape.url_escape('/userstats/')
            self.redirect("/user/login?next=%s&error=%s" % (next, error_msg))


class UserMiscHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        ajaxtarget = self.get_argument('ajaxtarget','')
        action = self.get_argument('action','')
        next=self.get_argument('next','/')
        msg='succeed'
        if action != '':
            if action=='chackemail':
                email=self.get_argument('email','')
                result,msg=yield self.exist(email=email)
                if result:
                    msg='Email is not usable'

        rendered = self.render_string('user/misc_%s.xml' % action, msg=msg,next=next)
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        self.write(rendered)
        self.finish()

class UserSpaceHandler(BaseHandler):
    @gen.coroutine
    def get(self,uid=None):
        user=yield self.get_user(uid)
        userstats=yield self.get_user_stats(uid)
        self.render("user/space.html",
            user=user,
            userstats = userstats,
            next=self.get_argument("next","/"),
        )

    @gen.coroutine
    def get_user_stats(self,uid):
        userstats=User.select().where(User.id==uid)
        raise gen.Return(userstats)

class UserHomeHandler(UserSpaceHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self,uid=None):
        user=self.get_current_user()
        logger.error(user)
        if not uid and not user:
            self.redirect('/user/login')
        userstats=yield self.get_user_stats(user['uid'])
        self.render("user/home.html",
            user=user,
            userstats = userstats,
            next=self.get_argument("next","/"),
        )

class UserTrackHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        user=self.get_current_user()
        remote_ip=self.request.remote_ip
        host = self.request.host

        user_agent = self.request.headers.get('User-Agent','')
        referer = self.request.headers.get('Referer','')
        x_forwarded_host=self.request.headers.get('X-Forwarded-Host','')
        if x_forwarded_host and host.startswith('127.0.0.1'):
            name = referer.replace('http://'+x_forwarded_host,'')
        else:
            name = referer.replace('http://'+host,'')
        delta=1
        #logger.error(str(self.request))
        #logger.error('|'.join([name,self.request.host]))



        stat = yield self.add_stats(name, delta)
        stat = yield self.add_track(name, host=remote_ip, ua=user_agent)

        self.set_header('Cache','No-Cache')
        self.set_header('Content-Type','image/jpeg')
        self.set_header('Etag',hashlib.sha1(str(time.time())).hexdigest())
        self.write(b'')
        self.finish()

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

class UserSettingsHandler(BaseHandler):
    DEFAULT_SETTINGS={
            'nickname':'',
    }

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        error = self.get_argument('error', '').strip()

        user=self.get_current_user()
        if user is None:
            uid=None
        else:
            uid = user['uid']

        if not uid:
            self.redirect('/user/login')
        else:
            self.render("user/settings.html",
                usersettings={},
                next=self.get_argument("next","/"),
                error=error
            )

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        errors=[]
        action = self.get_argument('action', '')
        user=self.get_current_user()
        if user:
            usersettings = self.DEFAULT_SETTINGS
        else:
            self.redirect('/user/login')

        if action=='profile':
            logger.debug('current user:%s, type:%s',user, type(user))
            nickname = self.get_argument('nickname', '').strip()
            if nickname:
                sql='''update ksforum.forum_users
                set nickname=%(nickname)s
                where id=%(uid)s'''
                r=yield momoko.Op(self.db.execute, sql, {'uid':user['uid'], 'nickname':nickname})
        elif action=='modifypassword':
            oldpassword = self.get_argument('password0', '').strip()
            newpassword1 = self.get_argument('password1', '').strip()
            newpassword2 = self.get_argument('password2', '').strip()
            if oldpassword and (newpassword1==newpassword2):
                sql='''update ksforum.forum_users
                set nickname=%(nickname)s
                where id=%(uid)s'''
                r=yield momoko.Op(self.db.execute, sql, {'uid':user['uid'], 'nickname':nickname})

                r=yield self.update_password(user['uid'], oldpassword, newpassword1)
        else:
            pass

        if errors:
            error_msg = tornado.escape.url_escape("Login Failed, username and password not match.")
            next = tornado.escape.url_escape('/user/home')
            self.redirect("/user/login?next=%s&error=%s" % (next, error_msg))
        else:
            record=yield self.get_user(user['uid'])
            user={'uid':record.id,'email':record.email,'username':record.username,'nickname':record.nickname,'retcode':0}
            self.set_current_user(user)
            self.redirect("/user/home")

    @gen.coroutine
    def update_password(self, uid, oldpassword, newpassword):
        sql = '''select password
        from public.users
        where id=%(user_id)s;
        '''
        result={'result':True,'error':None}

        if oldpassword:
            record=yield self.fetchone(sql, {'user_id':uid})
            password=record.password
            if password==self.encrypt(oldpassword):
                sql='''update public.users
                set password=%(newpassword)s
                where id=%(user_id)s
                '''
                r = yield self.fetchone(sql, {'user_id':uid, 'newpassword':self.encrypt(newpassword)})
                if not r:
                    result['result'] = False
                    result['error'] = 'update_password FAILED!!!'
        else:
            result['result'] = False
            result['error'] = 'update_password FAILED!!! invalid old password'
        raise gen.Return(result)
