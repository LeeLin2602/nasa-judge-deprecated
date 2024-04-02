from sqlalchemy.orm import scoped_session, sessionmaker
from utils import managed_session
from models import db

class Subtasks:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_subtask(self, problem_id, task_name, points):
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

    def query_subtask(self, problem_id):
        with managed_session(self.session_factory) as session:
            task_list = session.query(db.Subtask).filter_by(problem_id=problem_id, is_valid=1).all()
            task_data = [
                {
                    "id": task.id,
                    "task_name": task.task_name,
                    "points": task.points,
                } for task in task_list
            ]
            return task_data
