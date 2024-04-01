from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Problems:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_problems(self, problem_name,start_time, deadline):
        session = self.session_factory()
        try:
            problem = db.Problem(
                problem_name=problem_name,
                start_time=start_time,
                deadline=deadline
            )
            session.add(problem)
            session.commit()
            problem_id = problem.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            return problem_id
    
    def query_problem(self, problem_name):
        session = self.session_factory()
        try:
            problem = session.query(db.Problem).filter_by(problem_name=problem_name).first()
            problem_data = {
                "id": problem.id,
                "problem_name": problem.problem_name,
                "created_time": problem.created_time,
                "start_time": problem.start_time,
                "deadline": problem.deadline
            }
            return problem_data
        except Exception as e:
            raise e
        finally:
            session.close()