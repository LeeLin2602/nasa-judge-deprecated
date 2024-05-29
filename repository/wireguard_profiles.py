from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db, wg


class Profiles:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_profile(self, user_id):
        Id = 0
        with managed_session(self.session_factory) as session:
            new_profile = db.WireguardProfile(
                user_id=user_id,
                is_valid=True
            )
            print(f'New profile id: {new_profile.id}')
            
                
            session.add(new_profile)
            session.commit()
            Id = new_profile.id
        try:
            peer_config = wg.generate_wireguard_config(Id)
            print(peer_config)
        except Exception as e:
            session.rollback()
            raise e
        return new_profile.id

    def del_profile(self, profile_id):
        with managed_session(self.session_factory) as session:
            profile = (
                session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            )
            if profile:
                profile.valid = False
            session.commit()
            
    def query_profile(self, profile_id):
        with managed_session(self.session_factory) as session:
            profile = session.query(db.WireguardProfile).filter_by(id=profile_id).first()
            if profile and profile.is_valid:
                profile_data = {
                    "id": profile.id,
                    "is_valid": profile.is_valid,
                    "creation_date_time": profile.creation_date_time,
                    "user_id": profile.user_id,
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

    def query_profiles_by_user(self, user_id):
        with managed_session(self.session_factory) as session:
            profiles = session.query(db.WireguardProfile).filter_by(user_id=user_id).all()
            profile_data = [
                {
                    "id": profile.id,
                    "is_valid": profile.is_valid,
                    "creation_date_time": profile.creation_date_time,
                }
                for profile in profiles
            ]
        return profile_data
