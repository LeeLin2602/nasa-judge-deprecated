import logging
import secrets
from sqlalchemy import create_engine
from flask import Flask, request, g
from authlib.integrations.flask_client import OAuth

import config
import controllers.auth
from repository import users, Profiles
from service import AuthService
from models import wg


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

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
users = users.Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)


print(dir(controllers.auth))
app.register_blueprint(controllers.auth.blueprint)

@app.before_request
def load_user_identity():
    g.google_oauth = google_oauth
    g.auth_service = auth_service
    authorization_header = request.headers.get("Authorization")
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

if __name__ == "__main__":
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)
