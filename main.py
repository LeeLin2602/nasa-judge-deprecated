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
            "role": "ta",# g.user["role"],
            "uid": g.user["id"]
        }
        app.logger.info("User %s authenticated, %s %s", g.user["email"], g.user["id"], g.user["role"], extra=extra)
    else:
        g.user = None 

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
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_dir, "data")
problems = Problems(SQL_ENGINE, data_dir)

problem_service = ProblemService(logging, config.JWT_SECRET, problems)





from controllers import auth_bp, problem_bp, wg_bp # pylint: disable=wrong-import-position, unused-import, cyclic-import

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(problem_bp, url_prefix="/problems")
app.register_blueprint(wg_bp, url_prefix="/wg")
if __name__ == "__main__":
    app.run(debug=True, port=5000)
