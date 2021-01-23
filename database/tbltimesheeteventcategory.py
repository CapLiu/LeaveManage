from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date,Boolean


class TimeSheetEventCategory(Base):
    __tablename__ = 'timesheeteventcategory'
    id = Column(Integer,autoincrement=True,primary_key=True)
    # 类别名称
    eventcategoryname = Column(String,unique=True,nullable=False)
    # 创建时间
    createdate = Column(Date,nullable=False)

    def __repr__(self):
        return '<timesheeteventcategory(eventcategoryname=%s)>' % (self.eventcategoryname)