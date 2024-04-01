from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

from models import db

class Submissions:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))
    
    def add_submission(self, user_id, problem_id, submission_score):
        session = self.session_factory()
        try:
            submission = db.Submission(
                user_id=user_id,
                problem_id=problem_id,
                submission_score=submission_score,
            )
            session.add(submission)
            session.commit()
            submission_id = submission.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            return submission_id

    def query_submission(self, user_id, problem_id):
        session = self.session_factory()
        try:
            submission = session.query(db.Submission).filter_by(user_id=user_id, problem_id=problem_id).first()
            submission_data = {
                "id": submission.id,
                "user_id": submission.user_id,
                "problem_id": submission.problem_id,
                "submission_score": submission.submission_score,
                "submit_time": submission.submit_time
            }
            return submission_data
        except Exception as e:
            raise e
        finally:
            session.close()