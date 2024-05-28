import logging
import os
from flask import Flask, request, g
from authlib.integrations.flask_client import OAuth
from sqlalchemy import create_engine
import config

from repository import Users, Profiles, Problems
from service import AuthService, ProblemService


app = Flask(__name__)
# app.secret_key = secrets.token_urlsafe(16)
app.secret_key = config.SECRET_KEY

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
users = Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)
# subtasks = Subtasks(SQL_ENGINE)
problems = Problems(SQL_ENGINE)
# subtask_playbooks = SubtaskPlaybooks(SQL_ENGINE)

problem_service = ProblemService(logging, config.JWT_SECRET, problems)

project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_dir, "data")
# print(f"Data dir: {data_dir}\n\n\n\n\n\n")
# playbooks_path = f"./playbooks/1/"
# os.makedirs(playbooks_path, exist_ok=True)
# file_path = os.path.join(playbooks_path, "test.yaml")
# with open(file_path, "w") as f:
#     f.write("Hello, World!")

@app.before_request
def load_user_identity():
    authorization_header = request.headers.get("Authorization")
    g.users = users
    g.profiles = profiles
    g.problems = problems
    g.auth_service = auth_service
    g.problem_service = problem_service
    g.google_oauth = google_oauth
    g.project_dir = project_dir
    g.data_dir = data_dir
    if authorization_header:
        token = authorization_header.replace('Bearer ', '', 1)
        g.user = auth_service.authenticate_token(token)
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
    