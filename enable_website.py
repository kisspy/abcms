from models import db, Config

try:
    config=Config.select().where(Config.id==1).get()
except:
    config=Config(sitename='ABCcms', siteurl='http://localhost')
config.shutdown=False
config.save()
