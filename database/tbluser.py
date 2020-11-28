from database.tablebase import Base
from sqlalchemy import Column,String,Integer,Date,DateTime

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    usergroup = Column(String,nullable=False)
    state = Column(String)
    registerdate = Column(Date)
    lastlogintime = Column(DateTime)
    supervisor = Column(String)


    def __repr__(self):
        return '<user(username=%s,email=%s,registerdate=%s)>' % (self.username,self.email,self.registerdate)