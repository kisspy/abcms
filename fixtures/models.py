# -*- coding: utf-8 -*-

__author__ = 'Encore Hu, <huyoo353@126.com>'

from peewee import *
import datetime

#创建数据库实例
db = SqliteDatabase('abc.db')

#建议自己的项目使用一个新的基类，Model是peewee的基类
class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

    @classmethod
    def getOne(cls, *query, **kwargs):
       #为了方便使用，新增此接口，查询不到返回None，而不抛出异常
       try:
          return cls.get(*query,**kwargs)
       except DoesNotExist:
           return None

#AClass
class A(BaseModel):
    title = CharField()
    pinyin = CharField(null=True)

#示范一个表
class B(BaseModel):
    parent = ForeignKeyField(A, related_name='bset')
    title = CharField()
    pinyin = CharField(null=True)

#示范一个表
class C(BaseModel):
    parent = ForeignKeyField(B, related_name='cset')
    title = CharField()
    pinyin = CharField(null=True)
    content = TextField(null=True)

class User(BaseModel):

    username = CharField(max_length=64, unique=True)
    email    = CharField(max_length=128, unique=True)
    password = CharField(max_length=64)
    nickname = CharField(max_length=64, null=True)

    is_active = BooleanField(default=True)

class Link(BaseModel):
    title    = CharField(max_length=64, unique=True)
    url      = CharField(max_length=255, null=False, unique=True)
    desc     = CharField(max_length=255, null=True)
    category = CharField(max_length=32, null=True)

class Visit(BaseModel):
    user    = ForeignKeyField(User, related_name='user_visits')
    path    = CharField(max_length=255)
    ip      = CharField(max_length=64)

class Config(BaseModel):
    sitename    = CharField(max_length=64)
    siteurl     = CharField(max_length=128)
    ip      = CharField(max_length=64, null=True)
    domain    = CharField(max_length=64, null=True)
    title       = CharField(max_length=255, null=True)
    keywords    = CharField(max_length=255, null=True)
    description = CharField(max_length=511, null=True)
    copyright = CharField(max_length=511, null=True)
    shutdown  = BooleanField(default=False)
    reason    = CharField(max_length=255, null=True)
    logo    = CharField(max_length=255, null=True)

if __name__ == '__main__':
    db.connect()
    db.create_tables([A, B, C, User, Link, Config, Visit], safe=True)
