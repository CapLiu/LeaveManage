from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date,Boolean

class Vacation(Base):
    __tablename__ = 'vacation'
    id = Column(Integer,autoincrement=True,primary_key=True)
    # 请假人
    username = Column(String,nullable=False)
    # 假期类别
    vacationcategory = Column(String,nullable=False)
    # 起始日期
    startdate = Column(Date,nullable=False)
    # 起始日期是否为上午
    startdateMorning = Column(Boolean,nullable=False)
    # 终止日期
    enddate = Column(Date,nullable=False)
    # 终止日期是否为上午
    enddateMorning = Column(Boolean,nullable=False)
    # 请假理由
    reason = Column(String,nullable=False)


    def __repr__(self):
        return '<vacation(username=%s,vacationcategory=%s)>' % (self.username,self.vacationcategory)