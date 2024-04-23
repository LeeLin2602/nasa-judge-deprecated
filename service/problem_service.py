from datetime import timezone, datetime
import jwt

class ProblemService:
    def __init__(self, logger, jwt_secret, problems, subtasks, playbooks):
        self.logger = logger
        self.secret = jwt_secret
        self.problems = problems
        self.subtasks = subtasks
        self.playbooks = playbooks
        

    def create_problem(self, problem_name, start_time, deadline):
        problem = self.problems.query_problem(problem_name)
        if problem:
            self.logger.error(f"Problem already exists: {problem_name}")
            return None

        now = int(datetime.now(tz=timezone.utc).timestamp())
        problem_id = self.problems.create_problem(problem_name, start_time, deadline)
        return problem_id

    def delete_problem(self, problem_name):
        problem = self.problems.query_problem(problem_name)
        if not problem:
            self.logger.error(f"Problem not found: {problem_name}")
            return None

        self.problems.del_problem(problem_name)
        return problem_name
    
    def query_problem(self, problem_name):
        problem = self.problems.query_problem(problem_name)
        if not problem:
            self.logger.error(f"Problem not found: {problem_name}")
            return None

        return problem

    def query_all_problems(self):
        problems = self.problems.query_all_problems()
        return problems
    
    def update_problem(self, problem_id, problem_name, start_time, deadline):
        problem = self.problems.query_problem(problem_id)
        if not problem:
            self.logger.error(f"Problem not found: {problem_id}")
            return None

        self.problems.update_problem(problem_id, problem_name, start_time, deadline)
        return problem_id
    
    def query_all_subtasks(self, problem_id):
        subtasks = self.subtasks.query_all_subtasks(problem_id)
        return subtasks
    
    def query_all_playbooks(self, problem_id):
        subtasks = self.subtasks.query_all_subtasks(problem_id)
        return subtasks
    
    # subtask
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
    
    def update_subtask(self, task_id, task_name=None, points=None, is_valid=None):
        subtask = self.subtasks.query_subtask(task_id)
        if not subtask:
            self.logger.error(f"Subtask not found: {task_id}")
            return None
        self.subtasks.update_subtask(task_id, task_name, points, is_valid)
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