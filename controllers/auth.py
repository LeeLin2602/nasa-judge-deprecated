import secrets
from flask import url_for, jsonify, request, g

import authlib.integrations.base_client
from main import auth_service, app, google_oauth

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

@app.route("/whoami")
def whoami():
    if g.user:
        return jsonify({
            "email": g.user["email"],
            "role": g.user["role"],
        }), 200
    return jsonify({"error": "Unauthorized"}), 401
