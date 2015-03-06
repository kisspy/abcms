from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import Text, ForeignKey
from sqlalchemy import INTEGER

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence
from sqlalchemy import event
from sqlalchemy import DDL

Base = declarative_base()
#Base.metadata.schema = 'ksforum'

engine = create_engine('postgresql://huyoo:xyz2014@localhost:5432/cccc', convert_unicode=True, echo=True)

#event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS ksforum"))
'''
    #event.listen(
    #    Account.__table__,
    #    "after_create",
    #    DDL("ALTER SEQUENCE %(schema)s.%(table)s_id_seq RESTART WITH 10000;")
    #)
    # PLEASE ALWARS REMEMBER NOT UNCOMMENT THESE 2 LINES, IF YOU DONT KNOW WHAT YOU ARE DOING.
    # delete all tables!!!!
'''    
Session = sessionmaker(bind=engine)
session = Session()
sql="select id from  ksforum.forum_stats        where name='' and uid=0       limit 1"
params=None
cursor = session.execute(sql, {'username':'', 'password':''})
record = cursor.fetchone()
print record
for x in xrange(1000):
    cursor = session.execute(sql, {'username':'', 'password':''})
    record = cursor.fetchone()
print record

