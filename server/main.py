import sys
import platform
import os
sys.path.append(os.path.abspath('..'))
from setting.globalsettings import getconfig
from util.users.userutil import hasinit, inituser


import tornado.ioloop
import tornado.web

from server.apps.user_app.user_app import *
from server.apps.timesheet_app.timesheet_app import *

import requests

if platform.system() == 'Windows':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Index(BaseHandler):
    def get(self):
        indexpath = gettemplatepath('index.html')
        self.render(indexpath)

def make_app():
    routelist = [
        (r"/",Index),
        (r"/register",Register),
        (r"/createusergroup",CreateUserGroup),
        (r"/viewusergroup",ViewUserGroup),
        (r"/login",Login),
        (r"/personalinfo",PersonalInfo),
        (r"/logout",LogOut),
        (r"/usermanage",UserManage),
        (r"/approve",Approve),
        (r"/logoff",LogOff),
        (r"/filltimesheet/(year=\d*)&(month=\d*)",FillTimeSheet),
        (r"/viewtimesheet/(year=\d*)&(month=\d*)",ViewTimeSheet),
        (r"/createtimesheetevent",CreateTimeSheetEvent),
        (r"/timesheetindex",TimeSheetIndex),
        (r"/userorganization",UserOrganization),
        (r"/approvetimesheetindex",ApproveTimeSheetIndex),
        (r"/approvetimesheet/(year=\d*)&(month=\d*)&(employee=.*)",ApproveTimeSheet),
        (r"/approvetimesheet", ApproveTimeSheet),
        (r"/rejecttimesheet/(year=\d*)&(month=\d*)&(employee=.*)", RejectTimeSheet),
        (r"/createtimesheeteventcategory", CreateTimeSheetEventCategory),
        (r"/createvacationapply", CreateVacationApply),
        (r"/viewvacationapply",ViewVacationApply)
    ]
    return tornado.web.Application(routelist,cookie_secret='12f6352#527',autoreload=True,debug=True,template_path='D:\\LeaveManage\\server\\template')

if __name__ == '__main__':
    init_result = hasinit()
    if init_result == False:
        result = inituser()
        if result == 'Fail':
            print('初始化网站失败！')
            exit(0)
    app = make_app()
    port = int(getconfig('PORT'))
    app.listen(port)
    print('系统启动')
    tornado.ioloop.IOLoop.current().start()
