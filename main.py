from flask import Flask, jsonify, request
from repository import Profiles, Users, Problems, Submissions, Subtasks
from sqlalchemy import create_engine
from models import wg
import config
app = Flask(__name__)


connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PSWD}"
    f"@{config.MYSQL_HOST}/{config.MYSQL_DB}"
)
SQL_ENGINE = create_engine(connection_string)

profiles = Profiles(SQL_ENGINE)
profiles.add_profile()
print(profiles.query_profile(1))
profiles.del_profile(1)

users = Users(SQL_ENGINE)
users.add_user("roger")
print(users.query_user("roger"))

problems = Problems(SQL_ENGINE)
problems.add_problems("problem1", "2021-01-01", "2021-01-02")
print(problems.query_problem("problem1"))

submissions = Submissions(SQL_ENGINE)
submissions.add_submission(1, 1, 100)
print(submissions.query_submission(1, 1))

subtasks = Subtasks(SQL_ENGINE)
subtasks.add_subtask(1, "task1", 100)
subtasks.add_subtask(1, "task2", 100)
print(subtasks.query_subtask(1))
subtasks.del_subtask(1)
print(subtasks.query_subtask(1))

if __name__ == '__main__':
    app.run(debug=True)
    
