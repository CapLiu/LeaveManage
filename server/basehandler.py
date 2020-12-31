import tornado.web
from util.users.userutil import getusergroup


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        currentuser = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            currentuser = str(bytes_user,encoding='utf-8')
        return currentuser

    def render(self, template_name, **kwargs):
        currentuser = self.get_current_user()
        usergroup = getusergroup(currentuser)
        super(BaseHandler, self).render(template_name,currentuser=currentuser,currentusergroup=usergroup,**kwargs)
