from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Subtasks:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))
    
    def add_subtask(self, problem_id, task_name, points):
        session = self.session_factory()
        try:
            task = db.Subtask(
                problem_id=problem_id,
                task_name=task_name,
                points=points
            )
            session.add(task)
            session.commit()
            task_id = task.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            return task_id
        
    def del_subtask(self, task_id):
        session = self.session_factory()
        try:
            task = session.query(db.Subtask).filter_by(id=task_id).first()
            if task:
                task.is_valid = 0
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def query_subtask(self, problem_id):
        session = self.session_factory()
        try:
            task = session.query(db.Subtask).filter_by(problem_id=problem_id, is_valid=1).all()
            task_data = []
            for t in task:
                task_data.append({
                    "id": t.id,
                    "task_name": t.task_name,
                    "points": t.points
                })
            return task_data
        except Exception as e:
            raise e
        finally:
            session.close()