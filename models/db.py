from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    role = Column(String(255))
    submissions = relationship('Submission', back_populates='user')
    tasks = relationship('Tasks', back_populates='user')
    wireguard_profiles = relationship('WireguardProfile', back_populates='user')

class Problem(Base):
    __tablename__ = 'problem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_name = Column(String(255))
    created_time = Column(DateTime)
    deadline = Column(DateTime)
    submissions = relationship('Submission', back_populates='problem')
    tasks = relationship('Tasks', back_populates='problem')

class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    problem_id = Column(Integer, ForeignKey('problem.id'))
    submission_score = Column(Integer)
    timestamp = Column(DateTime)
    user = relationship('User', back_populates='submissions')
    problem = relationship('Problem', back_populates='submissions')

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255))
    points_credit = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    problem_id = Column(Integer, ForeignKey('problem.id'))
    is_passed = Column(Boolean)
    user = relationship('User', back_populates='tasks')
    problem = relationship('Problem', back_populates='tasks')

class WireguardProfile(Base):
    __tablename__ = 'wireguard_profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_valid = Column(Boolean)
    creation_date_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='wireguard_profiles')

