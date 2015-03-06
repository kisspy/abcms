#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import rsa
import binascii

from webclient import WebBrowser

import time

def get_timestamp():
    return ('%0.3f' % time.time()).replace('.','')

import urlparse
import traceback
import markdown

print WebBrowser
class FakeClient(WebBrowser):
    username = '330906552@qq.com'
    password = 'ijnokm'

    def __init__(self, base_url=None, *args, **kwargs):
        super(FakeClient, self).__init__(*args, **kwargs)
        if base_url:
            self.base_url=base_url
        else:
            self.base_url='http://localhost:8888'
        self.get(self.base_url)

    def get_xsrf(self, url=None):
            if not url:
                url='%s/user/login' % self.base_url
            p = re.compile('location\.replace\(\'(.*)\'\)') #2014-07-11 09:38:45 发现双引号换成了单引号
            p = re.compile(r'name="_xsrf" value="([\w\d\|]+)"/>')
            html=self.get(url)
            #print html
            #for x in p.findall(html):
            #    print x
            b=p.search(html)
            return b.group(1)

    def login(self):
        url = '{0}/user/login'.format(self.base_url,)
        data = {
            'email':self.username,
            'password':self.password,
            '_xsrf':self.get_xsrf(url),
        }

        headers = {
            'Referer':'{0}/user/login'.format(self.base_url,)
        }

        text = self.post(url, data = data, headers=headers )
        print '*'*80
        print text

    def logout(self):
        url = '{0}/user/logout'.format(self.base_url,)
        a=self._request(url)
        print a

    def new_thread(self, fid=1, title='', content=''):
        result = 0

        url = '{0}/bbs/f/{1}/newthread'.format(self.base_url, fid)

        _xsrf=self.get_xsrf(url)

        content_md  = content.encode('utf-8')
        content_html=(markdown.markdown(content)).encode('utf-8')

        data = {
            '_xsrf':_xsrf,
            'title':title,
            'content_md':content_md,
            'content_html':content_html,
        }


        a=self.post(url, data = data)
        #print a
        if a.startswith('ERROR'):
            print a

        return result


    def reply_thread(self, id, cid, message):
        '''#回复微博评论信息
        #个人理解：对某条消息id的评论cid的评论
        @id: 微博id
        @cid: 该微博的评论cid
        @message: 对该评论的回复消息, 即对评论进行评论.
        @return
        '''
        status = self.api.reply(id, cid, message)
        self.obj = status
        id = self.getAtt("id")
        text = self.getAtt("text")
        print("reply---"+ str(id) +":"+ text)
