from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db
import os

class Problems:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def create_problem(self, problem_name="newProblem"):
        with managed_session(self.session_factory) as session:
            problem = db.Problem(
                problem_name=problem_name
            )
            session.add(problem)
            session.commit()
            return problem.id

    def query_problem(self, problem_id):
        with managed_session(self.session_factory) as session:
            problem = (
                session.query(db.Problem).filter_by(id=problem_id, is_valid=True).first()
            )
            # if problem.is_valid is False:
            #     # print("Problem is not valid")
            #     return None  # Explicitly send a 404 error response
            if problem:
                problem_data = {
                    "problem_name": problem.problem_name,
                    "created_time": problem.created_time,
                    "start_time": problem.start_time,
                    "deadline": problem.deadline,
                    "subtasks": problem.subtasks,
                    "playbooks": problem.playbooks,
                    "allow_submission": problem.allow_submission,
                    # "is_valid": problem.is_valid 
                }
                return problem_data
            return None

    def del_problem(self, problem_id):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                problem.is_valid = 0
                session.commit()
                return problem.id
            return None

    def update_problem(self, problem_id, problem_name, allow_submission, 
                                start_time, deadline, subtasks, playbooks, 
                                new_subtasks, new_playbooks):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                # print("Problem ID: ", problem_id)
                # print("Start time: ", start_time)
                # print("Deadline: ", deadline)
                problem.problem_name = problem_name
                problem.allow_submission = allow_submission
                problem.start_time = start_time
                problem.deadline = deadline
                session.commit()

                # path of subtask scripts and playbooks
                subtasks_path = f"../data/subtask-scripts/{problem_id}"
                os.makedirs(subtasks_path, exist_ok=True)   
                playbooks_path = f"../data/playbooks/{problem_id}"
                os.makedirs(playbooks_path, exist_ok=True)

                # fetch existed subtasks
                # this subtask is a subtask object in db
                existing_subtasks = {subtask.id: subtask for subtask in problem.subtasks}
                
                # Update existing subtasks
                updated_subtask_ids = []
                for subtask in subtasks:
                    subtask_id = subtask.get("id")
                    updated_subtask_ids.append(subtask_id)
                    if subtask_id in existing_subtasks:
                        subtask_name = subtask.get("name")
                        subtask_content = subtask.get("content")
                        subtask_points = subtask.get("points")
                        self.update_subtask(subtask_id, subtask_name, subtask_content, subtask_points)
                        subtask_path = os.path.join(subtasks_path, f"{subtask_id}.sh")
                        with open(subtask_path, 'w') as file:
                            file.write(subtask_content)

                # Detect and handle deleted subtasks
                deleted_subtask_ids = set(existing_subtasks.keys()) - set(updated_subtask_ids)
                for subtask_id in deleted_subtask_ids:
                    del_subtask_id = self.del_subtask(subtask_id)
                

                # fetch existed playbooks
                # this playbook is a playbook object in db
                existing_playbooks = {playbook.id: playbook for playbook in problem.playbooks}
                
                # Update existing subtasks
                updated_playbook_ids = []
                for playbook in playbooks:
                    playbook_id = playbook.get("id")
                    updated_playbook_ids.append(playbook_id)
                    if playbook_id in existing_playbooks:
                        playbook_name = existing_playbooks[playbook_id].playbook_name
                        playbook_content = playbook.get("content")
                        playbook_path = os.path.join(playbooks_path, f"{playbook_name}.yaml")
                        with open(playbook_path, 'w') as file:
                            file.write(playbook_content)

                # Detect and handle deleted subtasks
                deleted_playbook_ids = set(existing_playbooks.keys()) - set(updated_playbook_ids)
                for playbook_id in deleted_playbook_ids:
                    del_playbook_id = self.del_playbook(playbook_id)

                # Handle new subtasks
                for new_subtask in new_subtasks:
                    new_subtask_name = new_subtask.get("name")
                    new_subtask_content = new_subtask.get("content")
                    new_subtask_points = new_subtask.get("points")
                    new_subtask_id = self.create_subtask(problem_id, new_subtask_name, new_subtask_points)
                    new_scipt_path = os.path.join(subtasks_path, f"{new_subtask_id}.sh")
                    # write script into file
                    with open(new_scipt_path, 'w') as file:
                        file.write(new_subtask_content)
                # Handle new playbooks
                for new_playbook in new_playbooks:
                    new_playbook_name = new_playbook.get("name")
                    new_playbook_content = new_playbook.get("content")
                    new_playbook_id = self.create_playbook(problem_id, new_playbook_name)
                    new_playbook_path = os.path.join(playbooks_path, f"{new_playbook_name}.yaml")
                    # write playbook into file
                    with open(new_playbook_path, 'w') as file:
                        file.write(new_playbook_content)
                return problem.id
            return None

    def query_all_problems(self):
        with managed_session(self.session_factory) as session:
            problems = session.query(db.Problem).all()
            problem_data = [
                {
                    "id": problem.id,
                    "problem_name": problem.problem_name
                }
                for problem in problems
            ]
            return problem_data
    # subtask
    def query_all_subtasks(self, problem_id):
        with managed_session(self.session_factory) as session:
            task_list = (
                session.query(db.Subtask)
                .filter_by(problem_id=problem_id, is_valid=True)
                .all()
            )
            # path of subtask scripts and playbooks
            subtasks_path = f"../data/subtask-scripts/{problem_id}"
            os.makedirs(subtasks_path, exist_ok=True)

            task_data = []
            for task in task_list:
                task_id = task.id
                subtask_path = os.path.join(subtasks_path, f"{task_id}.sh")
                with open(subtask_path, 'r') as file:
                    content = file.read()
                task_data.append({
                    "id": task_id,
                    "name": task.task_name,
                    "content": content,
                    "points": task.points,
                })
            # task_data = [
            #     {
            #         "id": task.id,
            #         "name": task.task_name,
            #         "content": 
            #         "points": task.points,
            #     }
            #     for task in task_list
            # ]
            return task_data
    # playbook
    def query_all_playbooks(self, problem_id):
        with managed_session(self.session_factory) as session:
            playbook_list = (
                session.query(db.SubtaskPlaybook)
                .join(db.Problem)  # Joins the Problem table4
                .filter(db.SubtaskPlaybook.problem_id == problem_id, db.Problem.is_valid == True)
                .filter_by(problem_id=problem_id, is_valid=True)
                .all()
            )
            playbooks_path = f"../data/playbooks/{problem_id}"
            os.makedirs(playbooks_path, exist_ok=True)
            playbook_data = []

            for playbook in playbook_list:
                playbook_name = playbook.playbook_name
                playbook_path = os.path.join(playbooks_path, f"{playbook_name}.yaml")
                with open(playbook_path, 'r') as file:
                    content = file.read()
                playbook_data.append({
                    "id": playbook.id,
                    "content": content,
                })

            # playbook_data = [
            #     {
            #         "id": playbook.id,
            #         "playbook_name": playbook.playbook_name,
            #     }
            #     for playbook in playbook_list
            # ]
            return playbook_data
    
    """
    #### subtask
    """
    def create_subtask(self, problem_id, task_name, points):
        with managed_session(self.session_factory) as session:
            task = db.Subtask(
                problem_id=problem_id,
                task_name=task_name,
                points=points,
            )
            session.add(task)
            session.commit()
            return task.id

    def del_subtask(self, task_id):
        with managed_session(self.session_factory) as session:
            task = session.query(db.Subtask).filter_by(id=task_id).first()
            if task:
                task.is_valid = 0
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
                    # read file from content file
                    # content: subtask.content,
                    "points": subtask.points
                }
            return None

    def update_subtask(self, task_id, task_name=None, contents = None, points=None):
        with managed_session(self.session_factory) as session:
            subtask = session.query(db.Subtask).filter_by(id=task_id).first()  
            if subtask:
                if task_name is not None:
                    subtask.task_name = task_name
                if points is not None:
                    subtask.points = points
                session.commit()
                # return {
                #     "id": subtask.id,
                #     "task_name": subtask.task_name,
                #     "points": subtask.points
                # }
                return subtask.id
        return None
    
    """
    #### playbook
    """

    def create_playbook(self, problem_id, playbook_name):
        """Add a new playbook to a problem."""
        with managed_session(self.session_factory) as session:
            playbook = db.SubtaskPlaybook(
                problem_id=problem_id,
                playbook_name=playbook_name,
            )
            session.add(playbook)
            # session.flush()  # Flush to ensure playbook.id is set
            session.commit()
            return playbook.id
        
    def query_playbook(self, playbook_id):
        """Retrieve all playbooks associated with a problem."""
        with managed_session(self.session_factory) as session:
            playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
            # if playbook.is_valid is False:
            #     return None
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
                playbook.is_valid = False
                # Option 2: Hard delete (remove from DB)
                # session.delete(playbook)
                session.commit()
                return {"status": "success", "id": playbook_id}
            return {"status": "error", "message": "Playbook not found"}
        
    # can not modify name of playbook 
    # def update_playbook(self, playbook_id, new_name):
    #     """Update the name of a playbook."""
    #     with managed_session(self.session_factory) as session:
    #         playbook = session.query(db.SubtaskPlaybook).filter_by(id=playbook_id).first()
    #         if playbook:
    #             playbook.playbook_name = new_name
    #             session.commit()
    #             return {"status": "success", "id": playbook_id}
    #         return {"status": "error", "message": "Playbook not found"}