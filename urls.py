from tornado.web import url
import tornado.web

from handlers.index import (
    IndexHandler,
    ManhuaHandler,
    TianhuodadaoHandler,
    QuanwenyueduHandler,
    XujiHandler,
    ZhoubianHandler,
    JueshitangmenHandler,
    JiushenHandler,
)

from handlers.abc import (
    AHandler,
    BHandler,
    CHandler,
)

from handlers.user import (
    LoginHandler,
    LogoutHandler,
    RegisterHandler,
    UserMiscHandler,
    UserSpaceHandler,
    ForgotPasswordHandler,
    ModifyPasswordHandler,
    UserSettingsHandler,
    UserHomeHandler,
    UserTrackHandler,
)

from handlers.admin import (
    AdminHandler,
    AdminSystemHandler,
    AdminThreadHandler,
    AdminUserHandler,
    AdminUserAddHandler,
    AdminChannelHandler,
    AdminVisitHandler,
    AdminLoginHandler,
    AdminLogoutHandler,
)

from handlers.help import (
    ContactusHandler,
    AboutusHandler,
    PrivacyHandler,
    DeclareHandler,
    LegalHandler,
    FAQHandler,
    WebsiteShutdownHandler,
)

url_patterns = [
    url(r'/', IndexHandler, name='index'),

    (r'/manhua/?', ManhuaHandler),
    (r'/tianhuodadao/?', TianhuodadaoHandler),
    (r'/quanwenyuedu/?', QuanwenyueduHandler),
    (r'/txt-xiazai/?', QuanwenyueduHandler),
    (r'/xuji/?', XujiHandler),
    (r'/zhoubian/?', ZhoubianHandler),
    (r'/jueshitangmen/?', JueshitangmenHandler),
    (r'/jiushen/?', JiushenHandler),
    (r'/(\d+)/?$', AHandler),
    (r'/(\d+)_(\d+)/?$', BHandler),
    (r'/(\d+)_(\d+)/(\d+)\.html', CHandler),


    #user
    (r"/user/login", LoginHandler),
    (r"/user/logout", LogoutHandler),
    (r"/user/register", RegisterHandler),
    (r"/user/forgotpassword", ForgotPasswordHandler),
    (r"/user/modifypassword", ModifyPasswordHandler),
    (r"/user/settings", UserSettingsHandler),
    (r"/user/misc", UserMiscHandler),
    (r"/user/home", UserHomeHandler),
    (r"/user[/]?", UserSpaceHandler),
    (r"/user/(\d+)", UserSpaceHandler),
    (r"/user/(\w+)", UserSpaceHandler),
    (r"/user", UserSpaceHandler),

    # website admin
    (r"/admin/?", AdminHandler),
    (r"/admin/system", AdminSystemHandler),
    (r"/admin/thread", AdminThreadHandler),
    (r"/admin/user", AdminUserHandler),
    (r"/admin/user/add", AdminUserAddHandler),
    (r"/admin/channel", AdminChannelHandler),
    (r"/admin/visit", AdminVisitHandler),
    (r"/admin/login", AdminLoginHandler),
    (r"/admin/logout", AdminLogoutHandler),

    #website help
    (r'/contactus/?', ContactusHandler),
    (r'/aboutus/?', AboutusHandler),
    (r'/privacy/?', PrivacyHandler),
    (r'/declare/?', DeclareHandler),
    (r'/legal/?', LegalHandler),
    (r'/faq/?', FAQHandler),
    (r'/shutdown/?', WebsiteShutdownHandler),

    #website friend link

    (r'/media/images/(.*)',tornado.web.StaticFileHandler, {'path': './media/images'},),
    #What if, we make a slight change here, negation with "^"? This would mean,
    #Tornado Web Server shouldn't load anything under images directory. Convenient!
    #(r'/images/^(.*)',tornado.web.StaticFileHandler, {'path': './images'},),


]
