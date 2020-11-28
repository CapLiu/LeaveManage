import datetime
from database.tbltimesheet import TimeSheet
from database.tbltimesheetevent import TimeSheetEvent
from database.tbltimesheetevent import TimeSheetEvent
from database.dbcore import session
from database.curd import insertdata,deletedata
from sqlalchemy import and_


class TimeSheetCalendar:
    def __init__(self,year,month):
        self.__year = year
        self.__month = month
        self.__week_list = []
        self.__monthday_map = {}

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
            if self.__monthday_map[monthday] == 0:
                self.__monthday_map[monthday] = 'Mon'
            elif self.__monthday_map[monthday] == 1:
                self.__monthday_map[monthday] = 'Tues'
            elif self.__monthday_map[monthday] == 2:
                self.__monthday_map[monthday] = 'Wed'
            elif self.__monthday_map[monthday] == 3:
                self.__monthday_map[monthday] = 'Thur'
            elif self.__monthday_map[monthday] == 4:
                self.__monthday_map[monthday] = 'Fri'
            elif self.__monthday_map[monthday] == 5:
                self.__monthday_map[monthday] = 'Sat'
            else:
                self.__monthday_map[monthday] = 'Sun'

    def __generateweeklist(self):
        extra_monthday_map = {}
        days = 0
        one_week = []
        oneday = datetime.timedelta(days=1)
        for monthday in self.__monthday_map:
            one_week.append(monthday)
            days += 1
            if days % 7 == 0:
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


def createtimesheetevent(eventcode,nickname):
    timesheetevent = session.query(TimeSheetEvent).filter(TimeSheetEvent.eventcode == eventcode)
    result = 'Fail'
    if type(timesheetevent) is not TimeSheetEvent:
        newtimesheetevent = TimeSheetEvent(eventcode=eventcode,nickname=nickname)
        result = insertdata(newtimesheetevent)
    return result