from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Users:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_user(self, name):
        session = self.session_factory()
        try:
            user = session.query(db.User).filter_by(name=name).first()
            if not user:
                user = db.User(name=name)
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def query_user(self, name):
        session = self.session_factory()
        try:
            user = session.query(db.User).filter_by(name=name).first()
            user_data = {
                "id": user.id,
                "name": user.name,
                "role": user.role
            }
            return user_data
        except Exception as e:
            raise e
        finally:
            session.close()

