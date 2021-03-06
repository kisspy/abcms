from wtforms import *
from wtforms.validators import *

from utils.util import MultiValueDict

class BaseForm(Form):
  def __init__(self, handler=None, obj=None, prefix='', formdata=None, **kwargs):
    if handler:
      formdata = MultiValueDict()
      for name in handler.request.arguments.keys():
        formdata.setlist(name, handler.get_arguments(name))
    Form.__init__(self, formdata, obj=obj, prefix=prefix, **kwargs)


# TODO Put your forms here

class HelloForm(BaseForm):
  planet = TextField('name', validators=[Required()])

class UserForm(BaseForm):
    username = TextField('username', validators=[Required()])
    email = TextField('email', validators=[Required()])
    password1 = TextField('password1', validators=[Required()])
    password2 = TextField('password2', validators=[Required()])
    gender = RadioField('gender', choices=[('male','male'),('female','female')], validators=[Required()])
