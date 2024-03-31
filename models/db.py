from sqlalchemy import Column, BigInteger, Boolean, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WireguardProfile(Base):
    __tablename__ = 'wireguard_profiles'

    profile_id = Column(BigInteger, primary_key=True, autoincrement=True)
    valid = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self):
        return f"<WireguardProfile(profile_id={self.profile_id}, valid={self.valid}, created_at='{self.created_at}')>"
