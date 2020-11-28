from database.dbcore import session
from database.curd import insertdata,deletedata
from database.tblusergroup import UserGroup
from database.tbluser import User
from datetime import date,datetime
import hashlib
from sqlalchemy import and_
import re
from util.email.emailutil import sendapprovemail


def createusergroup(groupname):
    usergroup = session.query(UserGroup).filter(UserGroup.groupname==groupname).first()
    result = 'Fail'
    if usergroup is None:
        # 用户组不存在，创建
        newusergroup = UserGroup(groupname=groupname,createdate=date.today())
        result = insertdata(newusergroup)
    return result

def encryption(password):
    m = hashlib.md5()
    byte_password = bytes(password,encoding='utf-8')
    m.update(byte_password)
    newpassword = m.hexdigest()
    return newpassword

def createuser(username,password,email,usergroup):
    result = 'Fail'
    if not validateemail(email):
        return result
    user = session.query(User).filter(User.username == username).first()
    if user is not None:
        return result
    user = session.query(User).filter(User.email == email).first()
    if user is not None:
        return result
    if usergroup == 'Root' or usergroup == 'Visitor':
        return result
    # user和email都不重复，则创建user
    password = encryption(password)
    newuser = User(username=username,password=password,email=email,usergroup=usergroup,state='WaitForApprove',registerdate=date.today(),
                   lastlogintime=datetime.now(),supervisor=username)
    result = insertdata(newuser)
    return result

def loginuser(username,password):
    password = encryption(password)
    user = session.query(User).filter(and_(User.username == username,User.password == password)).first()
    result = 'Fail'
    if type(user) is User:
        user.lastlogintime = datetime.now()
        result = insertdata(user)
    return result


def approveuser(username,usergroup):
    user = session.query(User).filter(User.username == username).first()
    result = 'Fail'
    if type(user) is User:
        user.state = 'Approved'
        user.usergroup = usergroup
        result = insertdata(user)
        if result == 'Success':
            sendapprovemail(user.username,usergroup,user.email)
    return result

def changeuserorganization(username,usergroup,supervisor):
    print(username)
    user = session.query(User).filter(User.username == username).first()
    result = 'Fail'
    if type(user) is User:
        user.usergroup = usergroup
        user.supervisor = supervisor
        result = insertdata(user)
        if result == 'Success':
            pass
            #sendapprovemail(user.username,usergroup,user.email)
    return result


def logoffuser(username):
    user = session.query(User).filter(User.username == username).first()
    result = 'Fail'
    if type(user) is User:
        user.state = 'Logoff'
        result = insertdata(user)
    return result


def getallusergroup():
    usergroup = session.query(UserGroup).filter(and_(UserGroup.groupname != 'Root',UserGroup.groupname != 'Visitor'))
    return usergroup

def getusergroup(username):
    user = session.query(User).filter(User.username == username).first()
    group = 'Visitor'
    if type(user) is User:
        group = user.usergroup
    return group

def validateemail(email):
    pattern_email = re.compile(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$')
    if pattern_email.match(email):
        return True
    return False

def inituser():
    # 创建Root用户组以及Root用户
    usergroup = session.query(UserGroup).filter(UserGroup.groupname == 'Root').first()
    result = 'Fail'
    if usergroup is None:
        # 用户组不存在，创建
        newusergroup = UserGroup(groupname='Root', createdate=date.today())
        result = insertdata(newusergroup)
        if result == 'Success':
            user = session.query(User).filter(User.username == 'Root').first()
            if user is None:
                rootuser = User(username='Root',password=encryption('123456'),email='584844970@qq.com',usergroup='Root',state='Approved',registerdate=date.today(),
                   lastlogintime=datetime.now())
                result = insertdata(rootuser)
                if result == 'Success':
                    usergroup = session.query(UserGroup).filter(UserGroup.groupname == 'Visitor').first()
                    if usergroup is None:
                        newusergroup = UserGroup(groupname='Visitor', createdate=date.today())
                        result = insertdata(newusergroup)
                        if result == 'Success':
                            print('系统初始化完成')
    return result


def hasinit():
    result = False
    usergroup = session.query(UserGroup).filter(UserGroup.groupname == 'Root').first()
    if type(usergroup) is not UserGroup:
        return result
    else:
        rootuser = session.query(User).filter(User.username == 'Root').first()
        if type(rootuser) is not User:
            return result
        else:
            result = True
    return result