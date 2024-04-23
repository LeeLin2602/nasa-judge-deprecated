import secrets
from flask import url_for, jsonify, request, g, redirect, session

import authlib.integrations.base_client
from main import auth_service
from app import app
import logging

app.secret_key = secrets.token_urlsafe(16)

@app.before_request
def load_user_identity():
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

# @app.route('/numbers/')
# def print_list():
#     return jsonify(list(range(5)))
@app.route("/get_login_url")
def get_login_url():
    redirect_uri = url_for("authorize", _external=True)
    # return jsonify({
    #     "auth_url": str(auth_url.location),
    # })
    return google_oauth.authorize_redirect(redirect_uri, return_json=True)
@app.route("/authorize")
def authorize():
    try:
        # token = google_oauth.authorize_access_token()
        # resp = google_oauth.get("account/verify_credentials.json")
        # resp.raise_for_status()
        # profile = resp.json()

        token = google_oauth.authorize_access_token()
        user = google_oauth.get('userinfo').json()
        session['user'] = user
        # do something with the token and profile
        return redirect('/')
    except authlib.integrations.base_client.errors.MismatchingStateError:
        return jsonify({"error": "MismatchingStateError"})

@app.route("/profile")
def show_profile():
    try:
        resp = google_oauth.get('user')
        resp.raise_for_status()
        profile = resp.json()
        return profile
        # user_info = resp.json()
        # token = auth_service.issue_token(user_info)
        # return token
    except authlib.integrations.base_client.errors.MismatchingStateError:
        return jsonify({"error": "MismatchingStateError"})

@app.route("/whoami")
def whoami():
    if g.user:
        return jsonify({
            "email": g.user["email"],
            "role": g.user["role"],
        }), 200
    return jsonify({"error": "Unauthorized"}), 401
