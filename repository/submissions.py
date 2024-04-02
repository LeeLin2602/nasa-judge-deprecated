from sqlalchemy.orm import scoped_session, sessionmaker
from utils import managed_session
from models import db

class Submissions:
    def __init__(self, sql_engine):
        self.session_factory = scoped_session(sessionmaker(bind=sql_engine))

    def add_submission(self, user_id, problem_id, submission_score):
        with managed_session(self.session_factory) as session:
            submission = db.Submission(
                user_id=user_id,
                problem_id=problem_id,
                submission_score=submission_score,
            )
            session.add(submission)
            return submission.id

    def query_submission(self, user_id, problem_id):
        with managed_session(self.session_factory) as session:
            submission = session.query(db.Submission).filter_by(
                user_id=user_id, problem_id=problem_id).first()
            if submission:
                return {
                    "id": submission.id,
                    "user_id": submission.user_id,
                    "problem_id": submission.problem_id,
                    "submission_score": submission.submission_score,
                    "submit_time": submission.submit_time
                }
            return None
