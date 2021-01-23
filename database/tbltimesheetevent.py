from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date,DateTime

class TimeSheetEvent(Base):
    __tablename__ = 'timesheetevent'
    id = Column(Integer,autoincrement=True,primary_key=True)
    eventcode = Column(String,nullable=False,unique=True)
    nickname = Column(String,nullable=False,unique=True)
    eventcategory = Column(String)

    def __repr__(self):
        return '<timesheetevent(eventcode=%s,state=%s)>' % (self.eventcode,self.nickname)