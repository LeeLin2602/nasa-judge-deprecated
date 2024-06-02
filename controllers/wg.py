from datetime import datetime  # Standard imports first
from flask import jsonify, request, g, Blueprint  # Third-party imports

wg_bp = Blueprint('wg', __name__)

@wg_bp.route("/profiles", methods=["GET"])
def query_all_profiles():
    print(f'User role: {g.user["role"]}')
    if g.user['role'] == 'ta':
        profiles = g.profiles.query_all_profiles()
    else:
        user_id = g.user['id']
        profiles = g.profiles.query_profiles_by_user(user_id)
    return jsonify(profiles)

@wg_bp.route("/profiles", methods=["POST"])
def create_profile():
    if not g.user:
        return jsonify({"error": "Unauthorized"}), 401

    # Only allow certain roles or users to create profiles if needed
    if g.user['role'] != 'user' and g.user['role'] != 'ta':
        return jsonify({"error": "Insufficient permissions"}), 403

    user_id = g.user['id']  # Get user ID from authenticated user context
    profile_id = g.profiles.add_profile(user_id)
    return jsonify({"profile_id": profile_id})

@wg_bp.route("/profiles/<int:profile_id>", methods=["GET"])
def query_profile(profile_id):
    if not g.user:
        return jsonify({"error": "Unauthorized"}), 401

    profile = g.profiles.query_profile(profile_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Only 'ta' or the profile's owner can access the profile
    if g.user['role'] != 'ta' and profile['user_id'] != g.user['id']:
        return jsonify({"error": "Unauthorized access"}), 403

    return jsonify(profile)

@wg_bp.route("/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    if g.user['role'] != 'ta' and g.user['role'] != 'user':
        return jsonify({"error": "Unauthorized"}), 403
    profile = g.profiles.query_profile(profile_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    if profile['user_id'] != g.user['id']:
        return jsonify({"error": "Unauthorized access"}), 403
    g.profiles.del_profile(profile_id)
    return jsonify(profile_id)
