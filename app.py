# app.py
from flask import Flask
from authlib.integrations.flask_client import OAuth

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
# Initialize OAuth with app
oauth = OAuth(app)
google_oauth = oauth.register(
    name="google",
    client_id='your_client_id',
    client_secret='your_client_secret',
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url='your_discovery_url',
)