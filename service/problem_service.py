class ProblemService:
    def __init__(self, logger, jwt_secret, problems):
        self.logger = logger
        self.secret = jwt_secret
        self.problems = problems

    def create_problem(self, problem_name="newProblem"):
        problem = self.problems.query_problem(problem_name)
        if problem:
            self.logger.error("Problem already exists: %s", problem_name)
            return None

        problem_id = self.problems.create_problem(problem_name)
        return problem_id

    def delete_problem(self, problem_id):
        problem = self.problems.query_problem(problem_id)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None

        self.problems.del_problem(problem_id)
        return problem_id

    def query_problem(self, problem_id):
        problem = self.problems.query_problem(problem_id)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None

        return problem

    def query_all_problems(self):
        return self.problems.query_all_problems()

    def update_problem(self, problem_id, problem_name, start_time, deadline):
        """
        Args:
        subtasks: list of json
        playbooks: list of json
        """
        problem = self.problems.query_problem(problem_id)
        if not problem:
            self.logger.error("Problem not found: %s", problem_id)
            return None
        success = self.problems.update_problem_details(
            problem_id, problem_name, start_time, deadline)
        if not success:
            return None
        return problem_id

    def update_subtasks(self, problem_id, subtasks, new_subtasks):
        self.problems.update_subtasks(problem_id, subtasks, new_subtasks)

    def update_playbooks(self, problem_id, playbooks, new_playbooks):
        self.problems.update_playbooks(problem_id, playbooks, new_playbooks)

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
