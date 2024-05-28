from datetime import datetime  # Standard imports first
import logging  # Import logging to use in the service class

# Removed unused imports
# import jwt
# from datetime import timezone
# from utils import managed_session, create_directory


class ProblemService:
    def __init__(self, logger, jwt_secret, problems):
        self.logger = logger
        self.secret = jwt_secret
        self.problems = problems

    def create_problem(self, problem_name="newProblem", data_dir=None):
        problem = self.problems.query_problem(problem_name, data_dir)
        if problem:
            self.logger.error("Problem already exists: %s", problem_name)
            return None

        problem_id = self.problems.create_problem(problem_name)
        return problem_id

    def delete_problem(self, problem_id, data_dir):
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None

        self.problems.del_problem(problem_id)
        return problem_id

    def query_problem(self, problem_id, data_dir):
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None

        return problem

    def query_all_problems(self):
        return self.problems.query_all_problems()

    def update_problem(self, problem_id, problem_name, allow_submissions, 
                        start_time, deadline, subtasks, playbooks, new_subtasks, 
                        new_playbooks, data_dir):
        """
        Args:
        subtasks: list of json
        playbooks: list of json
        """
        problem = self.problems.query_problem(problem_id, data_dir)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None
        success = self.problems.update_problem_details(problem_id, problem_name, 
                                                        allow_submissions, start_time, deadline)
        if not success:
            return None
        self.problems.update_subtasks(problem_id, subtasks, new_subtasks, data_dir)
        self.problems.update_playbooks(problem_id, playbooks, new_playbooks, data_dir)
        return problem_id

    def query_all_subtasks(self, problem_id):
        return self.problems.query_all_subtasks(problem_id)

    def query_all_playbooks(self, problem_id):
        return self.problems.query_all_playbooks(problem_id)

    def create_subtask(self, problem_id, task_name, points):
        return self.problems.create_subtask(problem_id, task_name, points)

    def delete_subtask(self, task_id):
        subtask = self.problems.query_subtask(task_id)
        if not subtask:
            self.logger.error("Subtask not found: %s", task_id)
            return None

        self.problems.del_subtask(task_id)
        return task_id

    def query_subtask(self, task_id):
        subtask = self.problems.query_subtask(task_id)
        if not subtask:
            self.logger.error("Subtask not found: %s", task_id)
            return None

        return subtask

    def update_subtask(self, task_id, task_name=None, points=None):
        subtask = self.problems.query_subtask(task_id)
        if not subtask:
            self.logger.error("Subtask not found: %s", task_id)
            return None
        self.problems.update_subtask(task_id, task_name, points)
        return task_id

    def create_playbook(self, problem_id, playbook_name):
        return self.problems.create_playbook(problem_id, playbook_name)

    def delete_playbook(self, playbook_id):
        playbook = self.problems.query_playbook(playbook_id)
        if not playbook:
            self.logger.error("Playbook not found: %s", playbook_id)
            return None

        self.problems.del_playbook(playbook_id)
        return playbook_id

    def query_playbook(self, playbook_id):
        playbook = self.problems.query_playbook(playbook_id)
        if not playbook:
            self.logger.error("Playbook not found: %s", playbook_id)
            return None

        return playbook

    def update_playbook(self, playbook_id, new_name):
        playbook = self.problems.query_playbook(playbook_id)
        if not playbook:
            self.logger.error("Playbook not found: %s", playbook_id)
            return None
        self.problems.update_playbook(playbook_id, new_name)
        return playbook_id
