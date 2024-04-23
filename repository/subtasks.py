from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db


class Subtasks:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def create_subtask(self, problem_id, task_name, points):
        with managed_session(self.session_factory) as session:
            task = db.Subtask(
                problem_id=problem_id,
                task_name=task_name,
                points=points,
            )
            session.add(task)
            return task.id

    def del_subtask(self, task_id):
        with managed_session(self.session_factory) as session:
            task = session.query(db.Subtask).filter_by(id=task_id).first()
            if task:
                task.is_valid = 0

    def query_subtask(self, task_id):
        with managed_session(self.session_factory) as session:
            subtask = session.query(db.Subtask).filter_by(id=task_id).first()
            if subtask:
                return {
                    "id": subtask.id,
                    "problem_id": subtask.problem_id,
                    "task_name": subtask.task_name,
                    "points": subtask.points,
                    "is_valid": subtask.is_valid
                }
            return None

    def update_subtask(self, task_id, task_name=None, points=None, is_valid=None):
        with managed_session(self.session_factory) as session:
            subtask = session.query(db.Subtask).filter_by(id=task_id).first()
            if subtask:
                if task_name is not None:
                    subtask.task_name = task_name
                if points is not None:
                    subtask.points = points
                if is_valid is not None:
                    subtask.is_valid = is_valid
                session.commit()
                return {
                    "id": subtask.id,
                    "task_name": subtask.task_name,
                    "points": subtask.points,
                    "is_valid": subtask.is_valid
                }
        return None