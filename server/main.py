import sys
import platform
import os
sys.path.append(os.path.abspath('..'))
import tornado.ioloop
import tornado.web
from tornado.web import url
from setting.globalsettings import getconfig,gettemplatepath
from util.users.userutil import createusergroup,getallusergroup,inituser,hasinit,createuser,getusergroup,loginuser,approveuser
from util.users.userutil import logoffuser
from database.dbcore import session
from database.tblusergroup import UserGroup
from database.tbluser import User
import datetime
from util.timesheet.timesheetutil import generateweekday,generatemonthday,filltimesheet,TimeSheetCalendar,TimeSheetViewer
from util.timesheet.timesheetutil import createtimesheetevent
from database.tbltimesheetevent import TimeSheetEvent
from database.tbltimesheet import TimeSheet
from sqlalchemy import and_
from util.users.userutil import changeuserorganization


if platform.system() == 'Windows':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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


class Index(BaseHandler):
    def get(self):
        indexpath = gettemplatepath('index.html')
        self.render(indexpath)


class Register(BaseHandler):
    def get(self):
        registerpath = gettemplatepath('register.html')
        usergroups = getallusergroup()
        self.render(registerpath,usergroups=usergroups)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        email = self.get_argument('email')
        usergroup = self.get_argument('usergroup')
        result = createuser(username,password,email,usergroup)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            result = '注册成功！'
        else:
            result = '注册失败！'
        self.render(resultpath, result=result)

class Login(BaseHandler):
    def get(self):
        loginpath = gettemplatepath('login.html')
        loginusername = self.get_secure_cookie('loginusername')
        loginuserpassword = self.get_secure_cookie('loginuserpassword')
        remembermevalue = self.get_secure_cookie('rememberme')
        remembermevalue = str(remembermevalue,encoding='utf-8')
        if loginusername is None and loginuserpassword is None:
            loginusername = ''
            loginuserpassword = ''
        self.render(loginpath,loginusername=loginusername,loginuserpassword=loginuserpassword,remembermevalue=remembermevalue)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        rememberme = self.get_argument('rememberme')
        if rememberme == 'on':
            self.set_secure_cookie('loginusername',username)
            self.set_secure_cookie('loginuserpassword',password)
            self.set_secure_cookie('rememberme','T')
        result = loginuser(username,password)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            result = '登录成功！'
            self.set_secure_cookie('currentuser',username)
            self.redirect('/')
        else:
            result = '用户名或密码错误！'
            self.render(resultpath, result=result)


class CreateUserGroup(BaseHandler):
    def get(self):
        createusergrouppath = gettemplatepath('createusergroup.html')
        self.render(createusergrouppath)

    def post(self):
        groupname = self.get_argument('usergroupname')
        result = 'Fail'
        if groupname != '':
            result = createusergroup(groupname)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            result = '成功创建用户组！'
        else:
            result = '创建用户组失败！'
        self.render(resultpath,result=result)

class ViewUserGroup(BaseHandler):
    def get(self):
        viewusergrouppath = gettemplatepath('viewusergroup.html')
        usergroups = session.query(UserGroup)
        self.render(viewusergrouppath,usergroups=usergroups)

class PersonalInfo(BaseHandler):
    def get(self):
        personalInfopath = gettemplatepath('personalinfo.html')
        currentuser = self.get_current_user()
        user = session.query(User).filter(User.username == currentuser).first()
        userInfo = {}
        if type(user) is User:
            userInfo['username'] = user.username
            userInfo['email'] = user.email
            userInfo['usergroup'] = user.usergroup
            userInfo['state'] = user.state
            userInfo['registerdate'] = user.registerdate
            userInfo['lastlogintime'] = user.lastlogintime
        self.render(personalInfopath,userInfo=userInfo)

class UserManage(BaseHandler):
    def get(self):
        usermanagepath = gettemplatepath('usermanage.html')
        users = session.query(User).filter(User.username != 'Root')
        usergroups = getallusergroup()
        userInfos = []
        for user in users:
            userInfo = {}
            usergrouplist = []
            userInfo['username'] = user.username
            userInfo['email'] = user.email
            userInfo['usergroup'] = user.usergroup
            if user.usergroup not in usergrouplist:
                usergrouplist.append(user.usergroup)
            userInfo['state'] = user.state
            userInfo['registerdate'] = user.registerdate
            userInfo['lastlogintime'] = user.lastlogintime
            if user.state == 'Approved':
                userInfo['submit'] = '/logoff'
            else:
                userInfo['submit'] = '/approve'
            userInfo['formid'] = user.id
            userInfo['groupid'] = str(user.id)+'_group'
            for othergroup in usergroups:
                if othergroup.groupname not in usergrouplist:
                    usergrouplist.append(othergroup.groupname)
            userInfo['usergrouplist'] = usergrouplist
            userInfos.append(userInfo)

        self.render(usermanagepath,userInfos=userInfos,usergroups=usergrouplist)


class Approve(BaseHandler):
    def post(self):
        userid = self.get_argument('userid')
        username = self.get_argument('username')
        usergroupid = userid + '_group'
        usergroup = self.get_argument(usergroupid)
        result = 'Fail'
        result = approveuser(username,usergroup)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            self.redirect('/usermanage')
        else:
            result = '操作失败！'
            self.render(resultpath,result=result)

class LogOff(BaseHandler):
    def post(self):
        username = self.get_argument('username')
        result = 'Fail'
        result = logoffuser(username)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            self.redirect('/usermanage')
        else:
            result = '操作失败！'
            self.render(resultpath,result=result)


class LogOut(BaseHandler):
    def get(self):
        self.clear_cookie('currentuser')
        self.redirect('/')


class TimeSheetIndex(BaseHandler):
    def get(self):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        timesheetindex = gettemplatepath('timesheetindex.html')
        year = datetime.datetime.today().year
        monthlist = range(1,13)
        monthoperation = {}
        for month in monthlist:
            timesheet = session.query(TimeSheet).filter(and_(TimeSheet.username == username,TimeSheet.year == year, TimeSheet.month == month)).first()
            if type(timesheet) is TimeSheet:
                if timesheet.state == 'Approved':
                    monthoperation[month] = 'View'
                else:
                    monthoperation[month] = 'Modify'
            else:
                monthoperation[month] = 'Fill'
        self.render(timesheetindex,year=year,monthlist=monthlist,monthoperation=monthoperation)


class FillTimeSheet(BaseHandler):
    def get(self,year,month):
        #today_date = datetime.datetime.today()
        year = int(year.split('=')[1])
        month = int(month.split('=')[1])
        timesheetcalendar = TimeSheetCalendar(year,month)
        timesheetpath = gettemplatepath('timesheet.html')
        timesheetcalendar.generatecalendar()
        monthday_map = timesheetcalendar.getmonthmap()
        week_list = timesheetcalendar.getweeklist()
        self.render(timesheetpath, monthdaymap=monthday_map,weeklist=week_list,year=year,month=month)

    def post(self,year,month):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        resultpath = gettemplatepath('timesheetfail.html')
        year = int(year.split('=')[1])
        month = int(month.split('=')[1])
        monthday_map = generatemonthday(year, month)
        business_list = {}
        for monthday in monthday_map:
            business_list[monthday] = self.get_argument(monthday)
        result = filltimesheet(username,year,month,business_list)
        print(result)
        if result == 'Fail':
            self.render(resultpath,result=result)
        else:
            redirecturl = '/viewtimesheet/year=' + str(year) + '&month=' + str(month)
            self.redirect(redirecturl)


class ViewTimeSheet(BaseHandler):
    def get(self,year,month):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        year = int(year.split('=')[1])
        month = int(month.split('=')[1])
        timesheetviewer = TimeSheetViewer(username=username,year=year,month=month)
        timesheetviewer.gettimesheetmap()
        timesheetcalendar = TimeSheetCalendar(year, month)
        timesheetcalendar.generatecalendar()
        monthday_map = timesheetcalendar.getmonthmap()
        week_list = timesheetcalendar.getweeklist()
        timesheet_map = timesheetviewer.gettimesheetmap()
        print(timesheet_map)
        timesheet_state = timesheetviewer.getstate()
        timesheet_approveuser = timesheetviewer.getapproveuser()
        timesheet_approvedate = timesheetviewer.getapprovedate()
        viewtimesheetpath = gettemplatepath('viewtimesheet.html')
        self.render(viewtimesheetpath, monthdaymap=monthday_map,weeklist=week_list,timesheetmap=timesheet_map,timesheetstate=timesheet_state,
                    timesheetapprovedate=timesheet_approvedate,timesheetapproveuser=timesheet_approveuser)


class CreateTimeSheetEvent(BaseHandler):
    def get(self):
        timesheeteventpath = gettemplatepath('createtimesheetevent.html')
        timesheetevents = session.query(TimeSheetEvent)

        self.render(timesheeteventpath,timesheetevents=timesheetevents)

    def post(self):
        eventcode = self.get_argument('eventcode')
        eventnickname = self.get_argument('eventnickname')
        result = createtimesheetevent(eventcode,eventnickname)
        resultpath = gettemplatepath('result.html')
        if result == 'Fail':
            self.render(resultpath,result=result)
        else:
            self.redirect('/createtimesheetevent')

class UserOrganization(BaseHandler):
    def get(self):
        userorganizationpath = gettemplatepath('userorganization.html')
        users = session.query(User).filter(User.username != 'Root')
        usergroups = getallusergroup()
        userInfos = []
        for user in users:
            usergrouplist = []
            usersupervisorlist = []
            userInfo = {}
            userInfo['username'] = user.username
            userInfo['usergroup'] = user.usergroup
            if user.usergroup not in usergrouplist:
                usergrouplist.append(user.usergroup)
            if user.supervisor not in usersupervisorlist and type(user.supervisor) is str:
                usersupervisorlist.append(user.supervisor)
            userInfo['formid'] = user.id
            userInfo['groupid'] = str(user.id)+'_group'
            userInfo['supervisorid'] = str(user.id) + '_supervisor'
            for othergroup in usergroups:
                if othergroup.groupname not in usergrouplist:
                    usergrouplist.append(othergroup.groupname)
            for otheruser in users:
                if otheruser.username not in usersupervisorlist:
                    usersupervisorlist.append(otheruser.username)
            userInfo['usergrouplist'] = usergrouplist
            userInfo['usersupervisorlist'] = usersupervisorlist
            userInfos.append(userInfo)
        self.render(userorganizationpath,userInfos=userInfos)

    def post(self):
        userid = self.get_argument('userid')
        username = self.get_argument('username')
        usergroupid = userid + '_group'
        usergroup = self.get_argument(usergroupid)
        supervisorid = userid + '_supervisor'
        supervisor = self.get_argument(supervisorid)
        result = 'Fail'
        result = changeuserorganization(username,usergroup,supervisor)
        resultpath = gettemplatepath('result.html')
        if result == 'Success':
            self.redirect('/userorganization')
        else:
            result = '操作失败！'
            self.render(resultpath,result=result)


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
        (r"/userorganization",UserOrganization)
    ]
    return tornado.web.Application(routelist,cookie_secret='12f6352#527',autoreload=True,debug=True)

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
    mainserver = tornado.ioloop.IOLoop.current()
    print('系统启动')
    mainserver.start()
