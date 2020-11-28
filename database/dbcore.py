from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setting.globalsettings import getconfig

conn_str = 'sqlite:///' + getconfig('DBPATH')

engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)
session = Session()