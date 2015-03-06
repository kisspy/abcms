# -*- coding: utf-8 -*-

from __future__ import division
import math
import datetime
import urlparse
import urllib
import hashlib
import tornado.web

from tornado import gen

from utils.message import Message

class Gravatar1(tornado.web.UIModule):
    def render(self, email, size=40, image_type='jpg'):
        url = u'http://gravatar.com/avatar/%s?s=%s.%s'
        email_hash = hashlib.md5(email).hexdigest()
        return url % (email_hash, size, image_type)

class Gravatar(tornado.web.UIModule):
    def render(self, email, size=40, image_type='jpg', onlyurl=False):
        if not email:
            image_url=self.handler.static_url("bbs/avatar/kisspy.png")
        else:
            email_hash = hashlib.md5(email).hexdigest()
            image_url="http://gravatar.com/avatar/{0}?s={1}.{2}".format(email_hash, size, image_type)
        if onlyurl:
            return image_url
        return '<img src="{0}">'.format(image_url)

class Hello(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

class Entry(tornado.web.UIModule):
    def render(self, entry, show_comments=False):
        return "something"

class DateTimeSince(tornado.web.UIModule):
    def render(self, date):
        #print type(date),date
        msg=str(date)
        if isinstance(date, datetime.datetime):
            #now=datetime.datetime.utcnow()
            now=datetime.datetime.now()
            delta=now-date
            #print delta
            if delta.days>30:
                return date.strftime('%Y-%m-%d')
            elif delta.days>7:
                msg='{0} weeks ago'.format(delta.days//7)
                return msg
            elif delta.days>0:
                msg='{0} days ago'.format(delta.days)
                return msg
            elif delta.days<0:
                return msg
            else:
                if delta.seconds>3600:
                    msg='{0} hours ago'.format(delta.seconds//3600)
                    return msg
                if delta.seconds>60:
                    msg='{0} minites ago'.format(delta.seconds//60)
                    return msg

                if delta.seconds>0:
                    msg='{0} seconds ago'.format(delta.seconds)
                    return msg
        else:
            return msg

class StdDate(tornado.web.UIModule):
    def render(self, date):
        #print type(date),date
        msg=str(date)
        if isinstance(date, datetime.datetime):
            return date.strftime('%Y-%m-%d')
        else:
            return msg

class StdDateTime(tornado.web.UIModule):
    def render(self, date):
        #print type(date),date
        msg=str(date)
        if isinstance(date, datetime.datetime):
            return date.strftime('%Y-%m-%d %H:%M')
        else:
            return msg

class ChineseDateTime(tornado.web.UIModule):
    def render(self, date):
        #print type(date),date
        msg=str(date)
        if isinstance(date, datetime.datetime):
            return date.strftime('%Y-%m-%d %H:%M')
        else:
            return msg

def update_querystring(url, **kwargs):
    base_url = urlparse.urlsplit(url)
    query_args = urlparse.parse_qs(base_url.query)
    query_args.update(kwargs)
    for arg_name, arg_value in kwargs.iteritems():
        if arg_value is None:
            if query_args.has_key(arg_name):
                del query_args[arg_name]

    query_string = urllib.urlencode(query_args, True)
    return urlparse.urlunsplit((base_url.scheme, base_url.netloc,
        base_url.path, query_string, base_url.fragment))

class Paginator(tornado.web.UIModule):
    """Pagination links display."""

    def render(self, page, page_size, results_count):
        if page_size<1:
            page_size =1
        pages = int(math.ceil(results_count / page_size)) if results_count else 0

        def get_page_url(page):
            # don't allow ?page=1
            if page <= 1:
                page = None
            return update_querystring(self.request.uri, page=page)

        next = page + 1 if page < pages else None
        previous = page - 1 if page > 1 else None

        return self.render_string('uimodules/pagination.html',
            page=page,
            pages=pages,
            page_size=page_size,
            next=next,
            previous=previous,
            get_page_url=get_page_url)

class ForumsMenu(tornado.web.UIModule):
    """ForumsMenu display."""
    def render(self, forums):
        return self.render_string('uimodules/forums_menu.html',forums=forums)


class WmdEditor(tornado.web.UIModule):
    """WmdEditor display."""
    def render(self, **kwargs):
        cm=kwargs.get('content_markdown',None)
        if not cm:
            kwargs.update({'content_markdown':''})

        preview=kwargs.get('preview',None)
        if not preview:
            kwargs.update({'preview':False})

        ti=kwargs.get('tabindex',None)
        if not ti:
            kwargs.update({'tabindex':2})
        return self.render_string('uimodules/wmdeditor.html', **kwargs)

class VisitorTrack(tornado.web.UIModule):
    """Used for user track stats."""
    def render(self, name='unkwon',ctype='', cid=0):
        '''render an image for visitor tracking

        ctype: content type, such as thread, post,...
        cid: content id, thread id, post id,...
        '''
        return '<img src="/hm?code={code}&data={data}" border="0" width="1" height="1">'.format(code=name, data=str(cid).encode('base64').strip().replace('=','_'))


class JoinQun(tornado.web.UIModule):
    def render(self, name='', idkey='', altname=''):
        '''join group compnont

        name: qun name...
        idkey: qunwpa idkey for join group
        '''
        return '<a target="_blank" href="http://shang.qq.com/wpa/qunwpa?idkey={idkey}"><img border="0" src="http://pub.idqqimg.com/wpa/images/group.png" alt="{alt}" title="{title}"></a>'.format(title=name, alt=name, idkey=idkey)

class HighlightKeyword(tornado.web.UIModule):
    def render(self, keyword=None):
        if not keyword:
            referer = self.request.headers.get('Referer','')
            q=[]
            if referer:
                base_url = urlparse.urlsplit(referer)
                query_args = urlparse.parse_qs(base_url.query)
                q=query_args.pop('q',[])

            if len(q):
                keyword=q[0]
            else:
                return ''

        kwargs={'q':keyword}
        return self.render_string('uimodules/highlightkeyword.html', **kwargs)

class ShowMessage(tornado.web.UIModule):
    def render(self, message=None, message_type='info'):
        kwargs={'message':message,'message_type':message_type}
        if not message:
            return ''
        return self.render_string('uimodules/message.html', **kwargs)

class ShowRedirectMessage(tornado.web.UIModule):
    def get_message(self, url, **kwargs):
        base_url = urlparse.urlsplit(url)
        query_args = urlparse.parse_qs(base_url.query)
        query_args.update(kwargs)

        messages=[]
        message_type='info'
        for arg_name, arg_value in query_args.iteritems():
            if arg_name in ['message','msg','info']:
                message_type='info'
            elif arg_name in ['error','err','error_message','error_msg','errormsg']:
                message_type='info'
            if arg_value:
                messages.append(arg_value)
        if messages:
            message='\n'.join(('<p>%s</p>' % msg for msg in messages))
        else:
            return None

        if message:
            return Message(message, message_type=message_type)
        else:
            return None

    def render(self, show_modal=False):
        message=self.get_message(self.request.uri)
        if not message:
            return ''
        kwargs={'message':message,'show_modal':show_modal,'id':'user_message'}
        return self.render_string('uimodules/redirect_message.html', **kwargs)
