import secrets
from sqlalchemy import create_engine
from flask import Flask, session
from flask_jwt_extended import JWTManager  # type: ignore

from repository import Profiles, Users, Problems, Submissions, Subtasks
import config

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.config["SESSION_COOKIE_NAME"] = "google-login-session"
app.config["PERMANENT_SESSION_LIFETIME"] = 300
app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)

jwt = JWTManager(app)

from controllers import auth

@app.route("/")
def homepage():
    email = session.get("email", None)
    return f"Hello, {email}!" if email else "Hello, Guest!"

connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PSWD}"
    f"@{config.MYSQL_HOST}/{config.MYSQL_DB}"
)

SQL_ENGINE = create_engine(connection_string)

profiles = Profiles(SQL_ENGINE)
profiles.add_profile()
# print(profiles.query_profile(1))
profiles.del_profile(1)

users = Users(SQL_ENGINE)
users.add_user("roger", "rogerdeng92@gmail.com")
print(users.query_user("roger"))

problems = Problems(SQL_ENGINE)
problems.add_problems("problem1", "2021-01-01", "2021-01-02")
# print(problems.query_problem("problem1"))

submissions = Submissions(SQL_ENGINE)
submissions.add_submission(1, 1, 100)
# print(submissions.query_submission(1, 1))

subtasks = Subtasks(SQL_ENGINE)
subtasks.add_subtask(1, "task1", 100)
subtasks.add_subtask(1, "task2", 100)
subtasks.del_subtask(1)

problems = Problems(SQL_ENGINE)
# problems.add_problems("problem2", "2021-01-01", "2021-01-02")
# print(problems.query_problem("problem2"))
# print(problems.query_all_problems())
# print(problems.query_subtask(1))

if __name__ == "__main__":
    app.run(debug=True)
