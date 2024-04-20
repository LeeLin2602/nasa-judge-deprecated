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
        problem_id = self.problems.add_problem(problem_name, start_time, deadline)
        return problem_id

    def delete_problem(self, problem_name):
        problem = self.problems.query_problem(problem_name)
        if not problem:
            self.logger.error(f"Problem not found: {problem_name}")
            return None

        self.problems.remove_problem(problem_name)
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

    # subtask

    # playbooks