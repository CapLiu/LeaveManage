from server.apps.basehandler import BaseHandler
from setting.globalsettings import gettemplatepath
import datetime
from util.timesheet.timesheetutil import generatemonthday,filltimesheet,TimeSheetCalendar,TimeSheetViewer
from util.timesheet.timesheetutil import createtimesheetevent
from database.tbltimesheetevent import TimeSheetEvent
from database.tbltimesheet import TimeSheet
from sqlalchemy import and_
from util.timesheet.timesheetutil import changetimesheetstate
from database.dbcore import session
from database.tbluser import User

# Modify by DS Liu 2021/1/23
from database.tbltimesheeteventcategory import TimeSheetEventCategory
from util.timesheet.timesheetutil import createtimesheeteventcategory
from util.timesheet.timesheetutil import createvacationapply,viewvacationapply

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
        timesheeteventcategory = session.query(TimeSheetEventCategory)

        self.render(timesheeteventpath,timesheetevents=timesheetevents,timesheeteventcategorys=timesheeteventcategory)

    def post(self):
        eventcode = self.get_argument('eventcode')
        eventnickname = self.get_argument('eventnickname')
        eventcategory = self.get_argument('eventcategory')
        result = createtimesheetevent(eventcode,eventnickname,eventcategory)
        resultpath = gettemplatepath('result.html')
        if result == 'Fail':
            self.render(resultpath,result=result)
        else:
            self.redirect('/createtimesheetevent')

class ApproveTimeSheetIndex(BaseHandler):
    def get(self):
        approveinfolist = []
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        approvetimesheetindexpath = gettemplatepath('approvetimesheetindex.html')
        employees = session.query(User).filter(User.supervisor==username)
        year = datetime.datetime.today().year
        for employee in employees:
            approveinfo = {}
            monthlist = []
            approveinfo['employee'] = employee.username
            timesheets = session.query(TimeSheet).filter(and_(TimeSheet.username == employee.username,TimeSheet.year == year))
            for timesheet in timesheets:
                monthlist.append(timesheet.month)
                approveinfo[timesheet.month] = timesheet.state
            approveinfo['monthlist'] = monthlist

            approveinfolist.append(approveinfo)
        self.render(approvetimesheetindexpath,approveinfolist=approveinfolist,year=year)


class ApproveTimeSheet(BaseHandler):
    def get(self,year,month,employee):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        year = int(year.split('=')[1])
        month = int(month.split('=')[1])
        employee = employee.split('=')[1]
        timesheetviewer = TimeSheetViewer(username=employee,year=year,month=month)
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
        approvetimesheetpath = gettemplatepath('approvetimesheet.html')
        self.render(approvetimesheetpath, monthdaymap=monthday_map,weeklist=week_list,timesheetmap=timesheet_map,timesheetstate=timesheet_state,
                    timesheetapprovedate=timesheet_approvedate,timesheetapproveuser=timesheet_approveuser,employee=employee,year=year,month=month)

    def post(self):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        employee = self.get_argument('employee')
        year = self.get_argument('year')
        month = self.get_argument('month')
        result = changetimesheetstate(username,employee,int(year),int(month),'Approved')
        resultpath = gettemplatepath('timesheetfail.html')
        if result == 'Success':
            self.redirect('/approvetimesheetindex')
        else:
            result = '操作失败！'
            self.render(resultpath,result=result)

class RejectTimeSheet(BaseHandler):
    def get(self,year,month,employee):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        employee = employee.split('=')[1]
        year = year.split('=')[1]
        month = month.split('=')[1]
        result = changetimesheetstate(username,employee,int(year),int(month),'Reject')
        resultpath = gettemplatepath('timesheetfail.html')
        if result == 'Success':
            self.redirect('/approvetimesheetindex')
        else:
            result = '操作失败！'
            self.render(resultpath,result=result)

# Modify by DS Liu 2021/1/23

class CreateTimeSheetEventCategory(BaseHandler):
    def get(self):
        timesheeteventpath = gettemplatepath('createtimesheeteventcategory.html')
        timesheeteventcategorys = session.query(TimeSheetEventCategory)
        self.render(timesheeteventpath,timesheeteventcategorys=timesheeteventcategorys)

    def post(self):
        categoryname = self.get_argument('categoryname')
        result = createtimesheeteventcategory(categoryname)
        resultpath = gettemplatepath('result.html')
        if result == 'Fail':
            self.render(resultpath,result=result)
        else:
            self.redirect('/createtimesheeteventcategory')

class CreateVacationApply(BaseHandler):
    def get(self):
        createvacationapplypath = gettemplatepath('createvacationapply.html')
        vacationcategory = session.query(TimeSheetEvent).filter(TimeSheetEvent.eventcategory == 'Vacation')
        self.render(createvacationapplypath, vacationcategory=vacationcategory)

    def post(self):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        category = self.get_argument('vacationcategory')
        startdate = self.get_argument('startdate')
        startdateMorning = self.get_argument('startdateMorning')
        enddate = self.get_argument('enddate')
        enddateMorning = self.get_argument('enddateMorning')
        timesum = self.get_argument('timesum')
        reason = self.get_argument('reason')
        currentuser = session.query(User).filter(User.username == username).first()
        approveuser = currentuser.supervisor
        result = createvacationapply(username,category,startdate,startdateMorning,
                                     enddate,enddateMorning,reason,timesum,
                                     approveuser,datetime.date.today(),'WaitForApprove')
        resultpath = gettemplatepath('result.html')
        self.render(resultpath, result=result)

class ViewVacationApply(BaseHandler):
    def get(self):
        username = ''
        bytes_user = self.get_secure_cookie('currentuser')
        if type(bytes_user) is bytes:
            username = str(bytes_user, encoding='utf-8')
        vacationlist = viewvacationapply(username)
        viewvacationapplypath = gettemplatepath('viewvacationapply.html')
        self.render(viewvacationapplypath,vacationlist=vacationlist)