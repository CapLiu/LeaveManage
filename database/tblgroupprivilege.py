from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date

class GroupPrivilege(Base):
    __tablename__ = 'groupprivilege'
    id = Column(Integer,autoincrement=True,primary_key=True)
    groupname = Column(String,unique=True,nullable=False)
    funclist = Column(String)

    def __repr__(self):
        return '<groupprivilege(groupname=%s,funclist=%s)>' % (self.groupname,self.funclist)