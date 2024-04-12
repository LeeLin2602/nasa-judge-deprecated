from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db


class Users:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_user(self, name, email):
        with managed_session(self.session_factory) as session:
            user = session.query(db.User).filter_by(name=name).first()
            if not user:
                user = db.User(name=name, email=email)
                session.add(user)

    def query_user(self, email):
        with managed_session(self.session_factory) as session:
            user = session.query(db.User).filter_by(email=email).first()
            if user:
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                }
                return user_data
            return None

    def query_all_users(self):
        with managed_session(self.session_factory) as session:
            users = session.query(db.User).all()
            user_data = [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                } for user in users
            ]
            return user_data
