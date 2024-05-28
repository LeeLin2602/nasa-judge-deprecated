from datetime import datetime  # Standard imports first
from flask import jsonify, request, g, Blueprint  # Third-party imports

problem_bp = Blueprint('problem', __name__)


@problem_bp.route("/", methods=["POST"])
def create_problem():
    problem_id = g.problem_service.create_problem("New Problem", g.data_dir)
    return jsonify({"problem_id": problem_id})


@problem_bp.route("/<string:problem_id>", methods=["DELETE"])
def delete_problem(problem_id):
    problem = g.problem_service.query_problem(problem_id, g.data_dir)
    if problem is None:
        return jsonify({"error": "Problem not found"}), 404
    problem_id = g.problem_service.delete_problem(problem_id, g.data_dir)
    return jsonify({"problem_id": problem_id})


@problem_bp.route("/<string:problem_id>", methods=["GET"])
def query_problem(problem_id):
    problem = g.problem_service.query_problem(problem_id, g.data_dir)
    if problem is None:
        return jsonify({"error": "Problem not found"}), 404
    return jsonify(problem)


@problem_bp.route("/<string:problem_id>", methods=["PUT"])
def update_problem(problem_id):
    problem = g.problem_service.query_problem(problem_id, g.data_dir)
    if problem is None:
        return jsonify({"error": "Problem not found"}), 404
    data = request.get_json()  # Get the JSON payload
    problem_name = data.get("problem_name")
    allow_submissions = data.get("allow_submissions")
    start_time_str = data.get("start_time")
    deadline_str = data.get("deadline")
    subtasks = data.get('subtasks', [])
    playbooks = data.get('playbooks', [])
    new_subtasks = data.get('newSubtasks', [])
    new_playbooks = data.get('newPlaybooks', [])
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S') if start_time_str else None
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S') if deadline_str else None

    problem_id = g.problem_service.update_problem(
        problem_id, problem_name, allow_submissions,
        start_time, deadline, subtasks, playbooks,
        new_subtasks, new_playbooks, g.data_dir
    )
    return jsonify({"problem_id": problem_id})


@problem_bp.route("/all_problems", methods=["GET"])
def query_all_problems():
    problems = g.problem_service.query_all_problems()
    if not problems:
        return jsonify({"error": "No problem is found"}), 404
    return jsonify(problems)
