# app.py
from flask import Flask
from authlib.integrations.flask_client import OAuth
import config
import uuid

def create_app():
    app = Flask(__name__)
    return app

# SECRET_KEY = str(uuid.uuid4().hex)
app = create_app()
# app.secret_key = config.SECRET_KEY
# # Initialize OAuth with app
# oauth = OAuth(app)
# google_oauth = oauth.register(
#     name="google",
#     client_id=config.GOOGLE_CLIENT_ID,
#     client_secret=config.GOOGLE_CLIENT_SECRET,
#     api_base_url="https://www.googleapis.com/oauth2/v1/",
#     userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
#     client_kwargs={"scope": "openid profile email"},
#     server_metadata_url=config.GOOGLE_DISCOVERY_URL,
# )

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['OAUTH2_PROVIDERS'] = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': config.GOOGLE_CLIENT_ID,
        'client_secret': config.GOOGLE_CLIENT_SECRET,
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v2/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'openid'
                    ],
    }
}