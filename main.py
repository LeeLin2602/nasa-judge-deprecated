import logging
from sqlalchemy import create_engine
from flask import Flask
from authlib.integrations.flask_client import OAuth

import config
from repository import users, Profiles
from service import AuthService
from models import wg

app = Flask(__name__)

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

print(wg.generate_wireguard_config(profiles.add_profile()))
print("\n\n\n\n\n\n\n")


users = users.Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)

from controllers import auth # pylint: disable=wrong-import-position, unused-import, cyclic-import

if __name__ == "__main__":
    app.run(debug=True)
    
