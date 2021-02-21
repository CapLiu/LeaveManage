import datetime
from database.tbltimesheet import TimeSheet
from database.tbltimesheetevent import TimeSheetEvent
from database.tbltimesheetevent import TimeSheetEvent
from database.dbcore import session
from database.curd import insertdata,deletedata
from sqlalchemy import and_
# Modify by DS Liu 2021/1/24
from database.tbltimesheeteventcategory import TimeSheetEventCategory
from database.tblvacation import Vacation


class TimeSheetCalendar:
    def __init__(self,year,month):
        self.__year = year
        self.__month = month
        self.__week_list = []
        self.__monthday_map = {}
        self.__weekday_map = {'0':'Mon',
                              '1':'Tues',
                              '2':'Wed',
                              '3':'Thur',
                              '4':'Fri',
                              '5':'Sat',
                              '6':'Sun'}

    def __generatemonthmap(self):
        firsttoday = datetime.datetime(self.__year, self.__month, 1)
        oneday = datetime.timedelta(days=1)
        if self.__month in [1, 3, 5, 7, 8, 10, 12]:
            while firsttoday.day <= 31 and firsttoday.month == self.__month:
                self.__monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                firsttoday += oneday
        elif self.__month in [4, 6, 9, 11]:
            while firsttoday.day <= 30 and firsttoday.month == self.__month:
                self.__monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                firsttoday += oneday
        elif self.__month == 2:
            if (self.__year % 4 == 0 and self.__year % 100 != 0) or self.__year % 400 == 0:
                while firsttoday.day <= 29 and firsttoday.month == 2:
                    self.__monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                    firsttoday += oneday
            else:
                while firsttoday.day <= 28 and firsttoday.month == 2:
                    self.__monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                    firsttoday += oneday
        else:
            print('Invalid month')
        for monthday in self.__monthday_map:
            self.__monthday_map[monthday] = self.__weekday_map[str(self.__monthday_map[monthday])]

    def __generateweeklist(self):
        extra_monthday_map = {}
        days = 0
        one_week = []
        oneday = datetime.timedelta(days=1)
        for monthday in self.__monthday_map:
            one_week.append(monthday)
            days += 1
            if len(one_week) == 7:
                self.__week_list.append(one_week)
                one_week = []
            elif days == len(self.__monthday_map):
                tmptimeinfo = monthday.split('-')
                tmpday = datetime.datetime(int(tmptimeinfo[0]), int(tmptimeinfo[1]), int(tmptimeinfo[2]))
                while len(one_week) < 7:
                    tmpday += oneday
                    one_week.append(tmpday.strftime('%Y-%m-%d'))
                    extra_monthday_map[tmpday.strftime('%Y-%m-%d')] = tmpday.weekday()
                self.__week_list.append(one_week)
            elif days == 1:
                # 每月1号若不是周一，则往前找到最近的周一
                if self.__monthday_map[monthday] != 'Mon':
                    tmptimeinfo = monthday.split('-')
                    tmpday = datetime.datetime(int(tmptimeinfo[0]), int(tmptimeinfo[1]), int(tmptimeinfo[2]))
                    while tmpday.weekday() != 0:
                        tmpday -= oneday
                        one_week.append(tmpday.strftime('%Y-%m-%d'))
                        extra_monthday_map[tmpday.strftime('%Y-%m-%d')] = tmpday.weekday()
                    one_week.reverse()
                if len(one_week) == 7:
                    self.__week_list.append(one_week)
                    one_week = []


        self.__monthday_map.update(extra_monthday_map)

    def generatecalendar(self):
        self.__generatemonthmap()
        self.__generateweeklist()

    def getmonthmap(self):
        return self.__monthday_map

    def getweeklist(self):
        return self.__week_list


class TimeSheetViewer:
    def __init__(self,username,year,month):
        self.__username = username
        self.__year = year
        self.__month = month
        self.__timesheetmap = {}
        self.__state = ''
        self.__approveuser = ''
        self.__approvedate = ''

    def __gettimesheetinfo(self):
        timesheet = session.query(TimeSheet).filter(and_(TimeSheet.username == self.__username,TimeSheet.year == self.__year, TimeSheet.month == self.__month)).first()
        timecalendar = TimeSheetCalendar(self.__year,self.__month)
        timecalendar.generatecalendar()
        monthmap = timecalendar.getmonthmap()
        print(type(timesheet))
        if type(timesheet) is TimeSheet:
            self.__state = timesheet.state
            self.__approveuser = timesheet.approveusername
            self.__approvedate = timesheet.approvedate
            for days in monthmap:
                tmpday = int(days.split('-')[2])
                tmpmonth = int(days.split('-')[1])
                dayinfo = 'day' + str(tmpday)
                if tmpmonth == self.__month:
                    event = session.query(TimeSheetEvent).filter(TimeSheetEvent.eventcode == getattr(timesheet,dayinfo,'')).first()
                    if type(event) is TimeSheetEvent:
                        self.__timesheetmap[days] = event.nickname
                    else:
                        self.__timesheetmap[days] = 'N/A'
                else:
                    self.__timesheetmap[days] = 'N/A'
        else:
            for days in monthmap:
                self.__timesheetmap[days] = 'N/A'

    def gettimesheetmap(self):
        self.__gettimesheetinfo()
        return self.__timesheetmap

    def getstate(self):
        return self.__state

    def getapproveuser(self):
        return self.__approveuser

    def getapprovedate(self):
        return self.__approvedate


def generateweekday(year,month,day):
    weekdaylist = []
    format_weekdaylist = []
    weekday_map = {}
    # 从周一到周日是一周
    tmp_today = datetime.datetime(year,month,day)
    oneday = datetime.timedelta(days=1)
    while datetime.datetime.weekday(tmp_today) > 0:
        tmp_today = tmp_today - oneday
        if tmp_today.date() not in weekdaylist:
            weekdaylist.append(tmp_today.date())
    if tmp_today.date() not in weekdaylist:
        weekdaylist.append(tmp_today.date())
    while datetime.datetime.weekday(tmp_today) < 6:
        tmp_today = tmp_today + oneday
        if tmp_today.date() not in weekdaylist:
            weekdaylist.append(tmp_today.date())
    weekdaylist.sort()
    for dateobject in weekdaylist:
        weekday_map[dateobject.weekday()] = dateobject.strftime('%Y-%m-%d')
        format_weekdaylist.append(dateobject.strftime('%Y-%m-%d'))
    print(weekday_map)
    return weekday_map


def generatemonthday(year,month):
    monthday_map = {}
    firsttoday = datetime.datetime(year, month, 1)
    oneday = datetime.timedelta(days=1)
    if month in [1,3,5,7,8,10,12]:
        while firsttoday.day <= 31 and firsttoday.month == month:
            monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
            firsttoday += oneday
    elif month in [4,6,9,11]:
        while firsttoday.day <= 30 and firsttoday.month == month:
            monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
            firsttoday += oneday
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            while firsttoday.day <= 29 and firsttoday.month == 2:
                monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                firsttoday += oneday
        else:
            while firsttoday.day <= 28 and firsttoday.month == 2:
                monthday_map[firsttoday.strftime('%Y-%m-%d')] = firsttoday.weekday()
                firsttoday += oneday
    else:
        print('Invalid month')
    for monthday in monthday_map:
        if monthday_map[monthday] == 0:
            monthday_map[monthday] = 'Mon'
        elif monthday_map[monthday] == 1:
            monthday_map[monthday] = 'Tues'
        elif monthday_map[monthday] == 2:
            monthday_map[monthday] = 'Wed'
        elif monthday_map[monthday] == 3:
            monthday_map[monthday] = 'Thur'
        elif monthday_map[monthday] == 4:
            monthday_map[monthday] = 'Fri'
        elif monthday_map[monthday] == 5:
            monthday_map[monthday] = 'Sat'
        else:
            monthday_map[monthday] = 'Sun'
    return monthday_map


def filltimesheet(username,year,month,business_list):
    timesheet = session.query(TimeSheet).filter(and_(TimeSheet.username == username,TimeSheet.year == year, TimeSheet.month == month)).first()
    result = 'Fail'
    if type(timesheet) is not TimeSheet:
        # Create new timesheet
        daysbusiness = {}
        newtimesheet = TimeSheet(username=username,approveusername='N/A',year=year,month=month,state='WaitForApprove',submitdate=datetime.date.today(),approvedate=datetime.date.today())
        for days in business_list:
            tmpday = int(days.split('-')[2])
            dayinfo = 'day' + str(tmpday)
            setattr(newtimesheet,dayinfo,business_list[days])
        result = insertdata(newtimesheet)
    else:
        # Recall
        for days in business_list:
            tmpday = int(days.split('-')[2])
            dayinfo = 'day' + str(tmpday)
            setattr(timesheet, dayinfo, business_list[days])
        timesheet.submitdate = datetime.datetime.today()
        result = insertdata(timesheet)
    return result


def createtimesheetevent(eventcode,nickname,eventcategory):
    timesheetevent = session.query(TimeSheetEvent).filter(TimeSheetEvent.eventcode == eventcode).first()
    result = 'Fail'
    if type(timesheetevent) is not TimeSheetEvent:
        newtimesheetevent = TimeSheetEvent(eventcode=eventcode,nickname=nickname,eventcategory=eventcategory)
        result = insertdata(newtimesheetevent)
    # Modify by DS Liu 2021/1/23
    else:
        timesheetevent.eventcategory = eventcategory
        result = insertdata(timesheetevent)
    return result


def changetimesheetstate(approver,employee,year,month,state):
    timesheet = session.query(TimeSheet).filter(and_(TimeSheet.username == employee,TimeSheet.year == year, TimeSheet.month == month)).first()
    result = 'Fail'
    if type(timesheet) is TimeSheet:
        timesheet.state = state
        timesheet.approveusername = approver
        timesheet.approvedate = datetime.datetime.today()
        result = insertdata(timesheet)
    return result


def createtimesheeteventcategory(categoryname):
    timesheeteventcategory = session.query(TimeSheetEventCategory).filter(TimeSheetEventCategory.eventcategoryname == categoryname)
    result = 'Fail'
    if type(timesheeteventcategory) is not TimeSheetEventCategory:
        newtimesheeteventcategory = TimeSheetEventCategory(eventcategoryname=categoryname,createdate=datetime.date.today())
        result = insertdata(newtimesheeteventcategory)
    return result


def createvacationapply(username,category,startdate,startdateMorning,enddate,enddateMorning,reason,timesum,approveuser,approvedate,state):
    result = 'Fail'
    if timesum == 0:
        result = 'Fail'
        return result
    if startdateMorning == 'Morning':
        startdateMorning = True
    else:
        startdateMorning = False
    if enddateMorning == 'Morning':
        enddateMorning = True
    else:
        enddateMorning = False

    if startdate == '':
        result = 'Fail'
        return result
    if enddate == '':
        result = 'Fail'
        return result

    startdateinfo = startdate.split('-')
    startdate_date = datetime.date(int(startdateinfo[0]),int(startdateinfo[1]),int(startdateinfo[2]))
    enddateinfo = enddate.split('-')
    enddate_date = datetime.date(int(enddateinfo[0]), int(enddateinfo[1]), int(enddateinfo[2]))
    newvacationapply = Vacation(username=username,vacationcategory=category,
                                startdate=startdate_date,
                                startdateMorning=startdateMorning,
                                enddate=enddate_date,
                                enddateMorning=enddateMorning,
                                reason=reason,
                                timesum=timesum,
                                approveuser=approveuser,
                                approvedate=approvedate,
                                state=state,
                                applydate=datetime.date.today())
    result = insertdata(newvacationapply)
    return result

def viewvacationapply(username):
    vacationlist = []
    vacationapplys = session.query(Vacation).filter(Vacation.username == username)
    for vacationapply in vacationapplys:
        vacationdict = {}
        vacationdict['id'] = vacationapply.id
        event = session.query(TimeSheetEvent).filter(TimeSheetEvent.eventcode == vacationapply.vacationcategory).first()
        if type(event) is TimeSheetEvent:
            vacationdict['category'] = event.nickname
        else:
            vacationdict['category'] = vacationapply.vacationcategory

        vacationdict['state'] = vacationapply.state
        vacationdict['startdate'] = vacationapply.startdate
        if vacationapply.startdateMorning == True:
            vacationdict['starttime'] = '9:00'
        else:
            vacationdict['starttime'] = '13:00'
        vacationdict['enddate'] = vacationapply.enddate
        if vacationapply.enddateMorning == True:
            vacationdict['endtime'] = '9:00'
        else:
            vacationdict['endtime'] = '13:00'
        vacationdict['timesum'] = vacationapply.timesum
        vacationlist.append(vacationdict)
    return vacationlist