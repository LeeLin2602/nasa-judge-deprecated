from sqlalchemy import TIMESTAMP, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    role = Column(String(255))
    submissions = relationship("Submission", back_populates="user")
    wireguard_profiles = relationship("WireguardProfile", back_populates="user")


class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_valid = Column(Boolean, default=True)
    problem_name = Column(String(255))
    created_time = Column(TIMESTAMP, default=func.now())
    start_time = Column(DateTime)
    deadline = Column(DateTime)
    submissions = relationship("Submission", back_populates="problem")
    subtasks = relationship("Subtask", back_populates="problem")


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    submission_score = Column(Integer)
    submit_time = Column(TIMESTAMP, default=func.now())
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")


class Subtask(Base):
    __tablename__ = "subtasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    task_name = Column(String(255))
    points = Column(Integer)
    is_valid = Column(Boolean, default=True)
    problem = relationship("Problem", back_populates="subtasks")


class WireguardProfile(Base):
    __tablename__ = "wireguard_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_valid = Column(Boolean, default=True)
    creation_date_time = Column(TIMESTAMP, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="wireguard_profiles")


class SubtaskResult(Base):
    __tablename__ = "subtaskResult"
    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    task_id = Column(Integer, ForeignKey("subtasks.id"))
    is_passed = Column(Boolean)
    subtask = relationship("Subtask")  # Corrected to 'Subtask'
