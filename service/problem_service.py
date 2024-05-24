from datetime import timezone, datetime
import jwt
from utils import managed_session, create_directory

class ProblemService:
    def __init__(self, logger, jwt_secret, problems, subtasks, playbooks):
        self.logger = logger
        self.secret = jwt_secret
        self.problems = problems
        self.subtasks = subtasks
        self.playbooks = playbooks
        

    def create_problem(self, problem_name="newProblem", data_dir=None):
        problem = self.problems.query_problem(problem_name, data_dir)
        if problem:
            self.logger.error(f"Problem already exists: {problem_name}")
            return None

        problem_id = self.problems.create_problem(problem_name)
        return problem_id

    def delete_problem(self, problem_id, data_dir):
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error(f"Problem not found: {problem_id}")
            return None

        self.problems.del_problem(problem_id)
        return problem_id
    
    def query_problem(self, problem_id, data_dir):
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error(f"Problem not found: {problem_id}")
            return None

        return problem

    def query_all_problems(self):
        problems = self.problems.query_all_problems()
        return problems
    
    # def update_problem(self, problem_id, problem_name, allow_submissions, 
    #                             start_time, deadline, subtasks, playbooks, 
    #                             new_subtasks, new_playbooks, data_dir):
        
    #     problem = self.problems.query_problem(problem_id, data_dir)
    #     if not problem:
    #         self.logger.error(f"Problem not found: {problem_id}")
    #         return None
    #     print('\n\nIN SERVICE: ')
    #     print(f'start_time: {start_time}')
    #     print(f'deadline: {deadline}')
    #     print(f"Problem name: {problem_name}\n\n\n")
    #     self.problems.update_problem(problem_id, problem_name, allow_submissions, 
    #                                     start_time, deadline, subtasks, playbooks, 
    #                                     new_subtasks, new_playbooks, data_dir)
    #     return problem_id

    def update_problem(self, problem_id, problem_name, allow_submissions, start_time, deadline, subtasks, playbooks, new_subtasks, new_playbooks, data_dir):
        """
        Args:
        subtasks: list of json
        playbooks: list of json
        """
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error(f"Problem not found: {problem_id}")
            return None
        print('\n\nIN SERVICE: ')
        print(f'start_time: {start_time}')
        print(f'deadline: {deadline}')
        print(f"Problem name: {problem_name}\n\n\n")
        success = self.problems.update_problem_details(problem_id, problem_name, allow_submissions, start_time, deadline)
        print(f"Success: {success}\n\n\n\n")
        if not success:
            return None
        self.problems.update_subtasks(problem_id, subtasks, new_subtasks, data_dir)
        self.problems.update_playbooks(problem_id, playbooks, new_playbooks, data_dir)
        return problem_id
    
    def query_all_subtasks(self, problem_id):
        subtasks = self.problems.query_all_subtasks(problem_id)
        return subtasks
    
    def query_all_playbooks(self, problem_id):
        subtasks = self.problems.query_all_playbooks(problem_id)
        return subtasks
    
    """
    #### subtask
    """
    def create_subtask(self, problem_id, task_name, points):
        subtask_id = self.subtasks.create_subtask(problem_id, task_name, points)
        return subtask_id


    def delete_subtask(self, task_id):
        subtask = self.subtasks.query_subtask(task_id)
        if not subtask:
            self.logger.error(f"Subtask not found: {task_id}")
            return None
        
        self.subtasks.del_subtask(task_id)
        return task_id
    

    
    def query_subtask(self, task_id):
        subtask = self.subtasks.query_subtask(task_id)
        if not subtask:
            self.logger.error(f"Subtask not found: {task_id}")
            return None

        return subtask
    
    def update_subtask(self, task_id, task_name=None, points=None):
        subtask = self.subtasks.query_subtask(task_id)
        if not subtask:
            self.logger.error(f"Subtask not found: {task_id}")
            return None
        self.subtasks.update_subtask(task_id, task_name, points)
        return task_id
    
    # playbooks
    def create_playbook(self, problem_id, playbook_name):
        playbook_id = self.playbooks.create_playbook(problem_id, playbook_name)
        return playbook_id


    def delete_playbook(self, playbook_id):
        playbook = self.playbooks.query_playbook(playbook_id)
        if not playbook:
            self.logger.error(f"playbook not found: {playbook_id}")
            return None
        
        self.playbooks.del_playbook(playbook_id)
        return playbook_id
    

    
    def query_playbook(self, playbook_id):
        playbook = self.playbooks.query_playbook(playbook_id)
        if not playbook:
            self.logger.error(f"playbook not found: {playbook_id}")
            return None

        return playbook
    
    def update_playbook(self, playbook_id, new_name):
        playbook = self.playbooks.query_playbook(playbook_id)
        if not playbook:
            self.logger.error(f"playbook not found: {playbook_id}")
            return None
        self.playbooks.update_playbook(playbook_id, new_name)
        return playbook_id