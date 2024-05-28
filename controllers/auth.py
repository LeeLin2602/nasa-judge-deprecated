import secrets
from flask import url_for, jsonify, g, Blueprint

import authlib.integrations.base_client

auth_bp = Blueprint('auth', __name__)
auth_bp.secret_key = secrets.token_urlsafe(16)


@auth_bp.route("/get_login_url")
def get_login_url():
    redirect_uri = url_for("auth.authorize", _external=True)
    auth_url = g.google_oauth.authorize_redirect(redirect_uri, return_json=True)
    return jsonify({
        "auth_url": str(auth_url.location),
    })

@auth_bp.route("/authorize")
def authorize():
    try:
        g.google_oauth.authorize_access_token()
        resp = g.google_oauth.get("userinfo")
        user_info = resp.json()
        # Debugging line to see what user_info contains
        print(f'User info: {user_info}\n')
        token = g.auth_service.issue_token(user_info)  # Pass user_info directly
        return token
    except authlib.integrations.base_client.errors.MismatchingStateError:
        return jsonify({"error": "MismatchingStateError"})

@auth_bp.route("/whoami")
def whoami():
    if g.user:
        return jsonify({
            "email": g.user["email"],
            "role": g.user["role"],
        }), 200
    return jsonify({"error": "Unauthorized"}), 401
    