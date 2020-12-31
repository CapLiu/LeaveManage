from server.basehandler import BaseHandler
from setting.globalsettings import gettemplatepath
from util.users.userutil import createusergroup,getallusergroup, createuser, loginuser,approveuser
from util.users.userutil import logoffuser
from database.tblusergroup import UserGroup
from database.tbluser import User
from database.dbcore import session

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