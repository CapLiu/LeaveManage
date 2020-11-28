from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date

class UserGroup(Base):
    __tablename__ = 'usergroup'
    id = Column(Integer,autoincrement=True,primary_key=True)
    groupname = Column(String,unique=True,nullable=False)
    createdate = Column(Date)

    def __repr__(self):
        return '<usergroup(groupname=%s,createdate=%s)>' % (self.groupname,self.createdate)