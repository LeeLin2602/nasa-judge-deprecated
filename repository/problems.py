import os  # Standard imports first
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker  # Third-party imports
from utils import managed_session  # First-party imports
from models import db

class Problems:
    def __init__(self, sql_engine, data_dir):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))
        self.data_dir = data_dir

    def create_problem(self, problem_name="newProblem"):
        with managed_session(self.session_factory) as session:
            problem = db.Problem(problem_name=problem_name)
            session.add(problem)
            session.commit()
            return problem.id

    def query_problem(self, problem_id):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id, is_valid=True).first()
            if problem:
                subtasks_list = self.query_all_subtasks(problem_id)
                playbooks_list = self.query_all_playbooks(problem_id)
                problem_data = {
                    "problem_name": problem.problem_name,
                    "created_time": problem.created_time,
                    "start_time": problem.start_time,
                    "deadline": problem.deadline,
                    "subtasks": subtasks_list,
                    "playbooks": playbooks_list,
                    "allow_submissions": problem.allow_submissions,
                }
                return problem_data
        return None

    def del_problem(self, problem_id):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                problem.is_valid = False
                session.commit()
                return problem.id
            return None

    def update_problem_details(self, problem_id, problem_name, start_time, deadline):
        current_time = datetime.now()
        allow_submissions = False

        if start_time <= current_time < deadline:
            allow_submissions = True

        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                problem.problem_name = problem_name
                problem.allow_submissions = allow_submissions
                problem.start_time = start_time
                problem.deadline = deadline
                session.commit()
                return True
        return False

    def update_subtasks(self, problem_id, subtasks, new_subtasks):
        if subtasks or new_subtasks:
            subtasks_path = os.path.join(self.data_dir, f"subtask-scripts/{problem_id}")
            os.makedirs(subtasks_path, exist_ok=True)

        existing_subtasks = {
            subtask['id']: subtask for subtask in self.query_all_subtasks(problem_id)
        }
        updated_subtask_ids = []
        for subtask in subtasks:
            subtask_id = subtask.get("id")
            updated_subtask_ids.append(subtask_id)
            if subtask_id in existing_subtasks:
                self.update_subtask(
                        subtask_id,
                        subtask.get("name"),
                        subtask.get("points"))
                with open(os.path.join(subtasks_path, f"{subtask_id}.sh"), \
                            'w', encoding='utf-8') as file:
                    file.write(subtask.get("content"))

        for subtask_id in set(existing_subtasks.keys()) - set(updated_subtask_ids):
            self.del_subtask(subtask_id)

        for new_subtask in new_subtasks:
            new_subtask_id = self.create_subtask(
                                problem_id,
                                new_subtask.get("name"),
                                new_subtask.get("points"))

            with open(os.path.join(subtasks_path, f"{new_subtask_id}.sh"), \
                        'w', encoding='utf-8') as file:
                file.write(new_subtask.get("content"))

    def update_playbooks(self, problem_id, playbooks, new_playbooks):
        if playbooks or new_playbooks:
            playbooks_path = os.path.join(
                                self.data_dir, f"playbooks/{problem_id}"
                            )
            os.makedirs(playbooks_path, exist_ok=True)

        existing_playbooks = {
            playbook['id']: playbook for playbook in self.query_all_playbooks(problem_id)
        }
        updated_playbook_ids = []
        for playbook in playbooks:
            playbook_id = playbook.get("id")
            updated_playbook_ids.append(playbook_id)
            if playbook_id in existing_playbooks:
                with open(os.path.join(
                                playbooks_path,
                                f"{existing_playbooks[playbook_id]['name']}.yaml"), \
                            'w', encoding='utf-8') as file:
                    file.write(playbook.get("content"))

        for playbook_id in set(existing_playbooks.keys()) - set(updated_playbook_ids):
            self.del_playbook(playbook_id)

        for new_playbook in new_playbooks:
            with open(os.path.join(playbooks_path, new_playbook.get("name")+".yaml"), \
                        'w', encoding='utf-8') as file:
                file.write(new_playbook.get("content"))

    def query_all_problems(self):
        with managed_session(self.session_factory) as session:
            problems = session.query(db.Problem).filter_by(is_valid=True).all()
            problem_data = [
                {"id": problem.id, "problem_name": problem.problem_name} for problem in problems
            ]
            return problem_data

    def query_all_subtasks(self, problem_id):
        with managed_session(self.session_factory) as session:
            task_list = session.query(db.Subtask) \
                        .filter_by(problem_id=problem_id, is_valid=True) \
                        .all()
            if task_list is None:
                return []
            subtasks_path = os.path.join(self.data_dir, f"subtask-scripts/{problem_id}")
            task_data = []
            for task in task_list:
                task_id = task.id
                subtask_path = os.path.join(subtasks_path, f"{task_id}.sh")
                with open(subtask_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                task_data.append({
                    "id": task_id, 
                    "name": task.task_name, 
                    "content": content, 
                    "points": task.points})
            return task_data

    def query_all_playbooks(self, problem_id):
        with managed_session(self.session_factory) as session:
            playbook_list = session.query(db.SubtaskPlaybook) \
                            .filter_by(problem_id=problem_id, is_valid=True) \
                            .all()
            if playbook_list is None:
                return []
            playbooks_path = os.path.join(self.data_dir, f"playbooks/{problem_id}")
            playbook_data = []
            for playbook in playbook_list:
                playbook_name = playbook.playbook_name
                playbook_path = os.path.join(playbooks_path, f"{playbook_name}.yaml")
                with open(playbook_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                playbook_data.append({
                        "id": playbook.id, 
                        "name": playbook_name, 
                        "content": content
                    })
            return playbook_data

    def create_subtask(self, problem_id, task_name, points):
        with managed_session(self.session_factory) as session:
            task = db.Subtask(problem_id=problem_id, task_name=task_name, points=points)
            session.add(task)
            session.commit()
            return task.id

    def del_subtask(self, task_id):
        with managed_session(self.session_factory) as session:
            task = session.query(db.Subtask).filter_by(id=task_id).first()
            if task:
                task.is_valid = False
                session.commit()
                return task.id
            return None

    def query_subtask(self, task_id):
        with managed_session(self.session_factory) as session:
            subtask = session.query(db.Subtask).filter_by(id=task_id).first()
            if subtask.is_valid is False:
                return None
            if subtask:
                return {
                    "id": subtask.id, 
                    "name": subtask.task_name, 
                    "points": subtask.points
                }
            return None

    def update_subtask(self, task_id, task_name=None, points=None):
        with managed_session(self.session_factory) as session:
            subtask = session.query(db.Subtask).filter_by(id=task_id).first()
            if subtask:
                if task_name is not None:
                    subtask.task_name = task_name
                if points is not None:
                    subtask.points = points
                session.commit()
                return subtask.id
        return None

    def create_playbook(self, problem_id, playbook_name):
        with managed_session(self.session_factory) as session:
            playbook = db.SubtaskPlaybook(problem_id=problem_id, playbook_name=playbook_name)
            session.add(playbook)
            session.commit()
            return playbook.id

    def query_playbook(self, playbook_id):
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            if playbook:
                return {"id": playbook.id, "playbook_name": playbook.playbook_name}
            return None

    def del_playbook(self, playbook_id):
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            if playbook:
                playbook.is_valid = False
                session.commit()
                return {"status": "success", "id": playbook_id}
            return {"status": "error", "message": "Playbook not found"}

    def update_playbook(self, playbook_id, new_name):
        """Update the name of a playbook."""
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            if playbook:
                playbook.playbook_name = new_name
                session.commit()
                return {"status": "success", "id": playbook_id}
            return {"status": "error", "message": "Playbook not found"}
