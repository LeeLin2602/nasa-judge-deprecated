from flask import redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth  # type: ignore
from flask_jwt_extended import create_access_token  # type: ignore
from flask_jwt_extended import jwt_required  # type: ignore
from flask_jwt_extended import get_jwt_identity  # type: ignore

from __main__ import app
import config

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=config.GOOGLE_DISCOVERY_URL,
)


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    _token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    email = user_info.get("email")
    session["email"] = email
    access_token = create_access_token(identity=email)
    return jsonify(access_token)


@app.route("/logout")
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    print(current_user)
    session.clear()
    return redirect(url_for("homepage"))
