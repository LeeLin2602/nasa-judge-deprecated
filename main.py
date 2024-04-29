from flask import Flask
from authlib.integrations.flask_client import OAuth

import config

from models import wg
from flask import url_for, jsonify, request, g
from instance import app, users, auth_service, profiles, problems, subtasks, subtask_playbooks, problem_service



from controllers import auth_bp, problem_bp # pylint: disable=wrong-import-position, unused-import, cyclic-import

@app.before_request
def load_user_identity():
    authorization_header = request.headers.get("Authorization")
    if authorization_header:
        token = authorization_header.replace('Bearer ', '', 1)
        g.user = auth_service.authenticate_token(token)
        g.users = users
        g.profiles = profiles
        g.problems = problems
        g.subtasks = subtasks
        g.subtask_playbooks = subtask_playbooks
        g.auth_service = auth_service
        g.problem_service = problem_service
        if g.user is None:
            return
        extra = {
            "email": g.user["email"],
            "role": g.user["role"],
        }
        app.logger.info("User %s authenticated", g.user["email"], extra=extra)
    else:
        g.user = None

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(problem_bp, url_prefix="/problems")
if __name__ == "__main__":
    app.run(debug=True)