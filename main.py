from flask import Flask
from authlib.integrations.flask_client import OAuth
from sqlalchemy import create_engine
import logging
import config

from models import wg
from flask import url_for, jsonify, request, g
from repository import users, Profiles, problems, subtasks, SubtaskPlaybooks
from service import AuthService, ProblemService



app = Flask(__name__)
# app.secret_key = config.SECRET_KEY
# Initialize OAuth with app
oauth = OAuth(app)
google_oauth = oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=config.GOOGLE_DISCOVERY_URL,
)

connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PSWD}"
    f"@{config.MYSQL_HOST}/{config.MYSQL_DB}"
)
SQL_ENGINE = create_engine(connection_string)
profiles = Profiles(SQL_ENGINE)
# print(wg.generate_wireguard_config(profiles.add_profile()))
# print("\n\n\n\n\n\n\n")
users = users.Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)
problems = problems.Problems(SQL_ENGINE)
subtasks = subtasks.Subtasks(SQL_ENGINE)
subtask_playbooks = SubtaskPlaybooks(SQL_ENGINE)

problem_service = ProblemService(logging, config.JWT_SECRET, problems, subtasks, subtask_playbooks)

@app.before_request
def load_user_identity():
    authorization_header = request.headers.get("Authorization")
    if authorization_header:
        token = authorization_header.replace('Bearer ', '', 1)
        g.user = auth_service.authenticate_token(token)
        g.users = users
        g.profiles = profiles
        g.problems = problems
        g.subtasks = subtasks
        g.subtask_playbooks = subtask_playbooks
        g.auth_service = auth_service
        g.problem_service = problem_service
        g.google_oauth = google_oauth
        if g.user is None:
            return
        extra = {
            "email": g.user["email"],
            "role": g.user["role"],
        }
        app.logger.info("User %s authenticated", g.user["email"], extra=extra)
    else:
        g.user = None

from controllers import auth_bp, problem_bp # pylint: disable=wrong-import-position, unused-import, cyclic-import

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(problem_bp, url_prefix="/problems")
if __name__ == "__main__":
    app.run(debug=True)