import logging
# app.py
from flask import Flask
from authlib.integrations.flask_client import OAuth
from sqlalchemy import create_engine
import config
import uuid
from repository import users, Profiles, problems, subtasks, SubtaskPlaybooks
from service import AuthService, ProblemService

def create_app():
    app = Flask(__name__)
    return app


# SECRET_KEY = str(uuid.uuid4().hex)
app = create_app()
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
users = users.Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)
problems = problems.Problems(SQL_ENGINE)
subtasks = subtasks.Subtasks(SQL_ENGINE)
subtask_playbooks = SubtaskPlaybooks(SQL_ENGINE)

problem_service = ProblemService(logging, config.JWT_SECRET, problems, subtasks, subtask_playbooks)

# app.config['OAUTH2_PROVIDERS'] = {
#     # Google OAuth 2.0 documentation:
#     # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
#     'google': {
#         'client_id': config.GOOGLE_CLIENT_ID,
#         'client_secret': config.GOOGLE_CLIENT_SECRET,
#         'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
#         'token_url': 'https://oauth2.googleapis.com/token',
#         'userinfo': {
#             'url': 'https://www.googleapis.com/oauth2/v2/userinfo',
#             'email': lambda json: json['email'],
#         },
#         'scopes': ['https://www.googleapis.com/auth/userinfo.email',
#                     'https://www.googleapis.com/auth/userinfo.profile',
#                     'openid'
#                     ],
#     }
# }