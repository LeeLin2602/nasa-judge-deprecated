from flask import url_for, session, jsonify
from flask import request, g
import secrets

import authlib.integrations.base_client
from __main__ import auth_service, app, google_oauth
import config

app.secret_key = secrets.token_urlsafe(16)



@app.before_request
def load_user_identity():
    pass

@app.route("/get_login_url")
def get_login_url():
    redirect_uri = url_for("authorize", _external=True)
    auth_url = google_oauth.authorize_redirect(redirect_uri, return_json=True)
    return jsonify({
        "auth_url": str(auth_url.location),
    })

@app.route("/authorize")
def authorize():
    try:
        google_oauth.authorize_access_token()
        resp = google_oauth.get("userinfo")
        user_info = resp.json()
        token = auth_service.issue_token(user_info)
        return token
    except authlib.integrations.base_client.errors.MismatchingStateError:
        return jsonify({"error": "MismatchingStateError"})
