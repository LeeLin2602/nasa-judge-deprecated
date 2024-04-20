import secrets
from flask import Blueprint, url_for, jsonify, request, g

import authlib.integrations.base_client
import config

blueprint = Blueprint('blueprint', __name__)


@blueprint.route("/get_login_url")
def get_login_url():
    redirect_uri = config.URL_BASE + "authorize" #url_for("authorize", _external=True)
    auth_url = g.google_oauth.authorize_redirect(redirect_uri, return_json=True)
    return jsonify({
        "auth_url": str(auth_url.location),
    })

@blueprint.route("/authorize")
def authorize():
    try:
        g.google_oauth.authorize_access_token()
        resp = g.google_oauth.get("userinfo")
        user_info = resp.json()
        token = g.auth_service.issue_token(user_info)
        return token
    except authlib.integrations.base_client.errors.MismatchingStateError:
        return jsonify({"error": "MismatchingStateError"})

@blueprint.route("/whoami")
def whoami():
    if g.user:
        return jsonify({
            "email": g.user["email"],
            "role": g.user["role"],
        }), 200
    return jsonify({"error": "Unauthorized"}), 401
