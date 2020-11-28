from database.dbcore import session
from sqlalchemy.exc import DBAPIError,SQLAlchemyError

def insertdata(dbobject):
    result = 'Fail'
    session.add(dbobject)
    try:
        session.commit()
        result = 'Success'
    except DBAPIError as e:
        print(e)
        session.rollback()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        return result

def deletedata(dbobject):
    result = 'Fail'
    session.delete(dbobject)
    try:
        session.commit()
        result = 'Success'
    except DBAPIError as e:
        print(e)
        session.rollback()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        return result