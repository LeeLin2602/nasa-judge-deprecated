from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db


class Profiles:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_profile(self):
        with managed_session(self.session_factory) as session:
            profile = db.WireguardProfile()
            session.add(profile)
            return profile.id

    def del_profile(self, profile_id):
        with managed_session(self.session_factory) as session:
            profile = (
                session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            )
            if profile:
                profile.valid = False

    def query_profile(self, profile_id):
        with managed_session(self.session_factory) as session:
            profile = (
                session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            )
            if profile:
                profile_data = {
                    "id": profile.id,
                    "is_valid": profile.is_valid,
                    "creation_date_time": profile.creation_date_time,
                }
                return profile_data
            return None

    def query_all_profiles(self):
        with managed_session(self.session_factory) as session:
            profiles = session.query(db.WireguardProfile).all()
            profile_data = [
                {
                    "id": profile.id,
                    "is_valid": profile.is_valid,
                    "creation_date_time": profile.creation_date_time,
                }
                for profile in profiles
            ]
            return profile_data
