from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Profiles:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_profile(self):
        session = self.session_factory()
        try:
            profile = db.WireguardProfile()
            session.add(profile)
            session.commit()
            profile_id = profile.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            return profile_id

    def del_profile(self, profile_id):
        session = self.session_factory()
        try:
            profile = session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            if profile:
                profile.valid = False
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def query_profile(self, profile_id):
        session = self.session_factory()
        try:
            profile = session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            profile_data = {
                "id": profile.id,
                "is_valid": profile.is_valid,
                "creation_date_time": profile.creation_date_time,
            }
            return profile_data
        except Exception as e:
            raise e
        finally:
            session.close()
