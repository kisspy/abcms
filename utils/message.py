
class Message(object):
    code=0
    message=''
    body=''
    title=''
    level='info' # debug, info, warn(alert), error
    redirect_url='#' # after user click ok/cancel, jump to redirect_url

    def __init__(self, message, code=0, message_title='', level='info', message_type='info'):
        self.message=message
        self.body=message
        self.title=message_title
        self.code=code
        self.level=(message_type or level)
