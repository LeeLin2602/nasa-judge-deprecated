from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db


class SubtaskPlaybooks:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))
    
    def create_playbook(self, problem_id, playbook_name):
        """Add a new playbook to a problem."""
        with managed_session(self.session_factory) as session:
            playbook = db.SubtaskPlaybook(
                problem_id=problem_id,
                playbook_name=playbook_name,
            )
            session.add(playbook)
            session.flush()  # Flush to ensure playbook.id is set
            session.commit()
            return playbook.id
        
    def query_playbook(self, playbook_id):
        """Retrieve all playbooks associated with a problem."""
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).all()
            if playbook:
                playbook_data = {
                        "id": playbook.id,
                        "playbook_name": playbook.playbook_name,
                    }
                return playbook_data
            
            return None
        
    def del_playbook(self, playbook_id):
        """Mark a playbook as invalid or remove it from the database."""
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            if playbook:
                # Option 1: Soft delete (mark as invalid)
                playbook.is_valid = 0
                # Option 2: Hard delete (remove from DB)
                # session.delete(playbook)
                # session.commit()
                return {"status": "success", "id": playbook_id}
            return {"status": "error", "message": "Playbook not found"}
    def update_playbook(self, playbook_id, new_name):
        """Update the name of a playbook."""
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            if playbook:
                playbook.playbook_name = new_name
                return {"status": "success", "id": playbook_id}
            return {"status": "error", "message": "Playbook not found"}
