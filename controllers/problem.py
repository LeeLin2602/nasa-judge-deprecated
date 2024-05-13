from flask import url_for, jsonify, request, g, Blueprint, render_template
from datetime import datetime
# from service.problem_service import problem_service
# from instance import problem_service

# check user role at here 
# parse json
"""
#####
for testing
#####
"""
problem_bp = Blueprint('problem', __name__)

# @problem_bp.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @problem_bp.route('/<string:invalid_path>')
# def handle_unmatched(*args, **kwargs):
#     return jsonify({"error": "Api not found"}), 404


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
    print(f"Problem: {problem}\n\n\n\n\n\n\n")
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
    if start_time_str:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    if deadline_str:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
    print("Subtasks: ", subtasks)
    print("Playbooks: ", playbooks)
    print("New problem: ", problem_name)
    print("New start time: ", start_time)
    print("New deadline: ", deadline)
    problem_id = g.problem_service.update_problem(problem_id, problem_name, allow_submissions, 
                                                    start_time, deadline, subtasks, playbooks, 
                                                    new_subtasks, new_playbooks, g.data_dir)
    return jsonify({"problem_id": problem_id})


"""
#####
Query all problems, subtasks, playbooks
#####
"""

@problem_bp.route("/all_problems", methods=["GET"])
def query_all_problems():
    problems = g.problem_service.query_all_problems()
    if not problems:
        return jsonify({"error": "No problem is found"}), 404
    return jsonify(problems)

# @problem_bp.route("/<string:problem_id>/all_subtasks", methods=["GET"])
# def query_all_subtasks(problem_id):
#     subtasks = g.problem_service.query_all_subtasks(problem_id)
#     if not subtasks:
#         return jsonify({"error": "No subtask is found"}), 404
#     return jsonify(subtasks)

# @problem_bp.route("/<string:problem_id>/all_playbooks", methods=["GET"])
# def query_all_playbooks(problem_id):
#     playbooks = g.problem_service.query_all_playbooks(problem_id)
#     if not playbooks:
#         return jsonify({"error": "Playbooks not found"}), 404   
#     return jsonify(playbooks)

"""
#####
Subtasks 
#####
"""

# @problem_bp.route("/<string:problem_id>/subtasks", methods=["POST"])
# def create_subtask(problem_id):
#     task_name = request.json.get("task_name")
#     points = request.json.get("points")
#     subtask_id = g.problem_service.create_subtask(problem_id, task_name, points)
#     return jsonify({"subtask_id": subtask_id})

# @problem_bp.route("/subtasks/<string:task_id>", methods=["GET"])
# def query_subtask(task_id):
#     subtask = g.problem_service.query_subtask(task_id)
#     if subtask is None:
#         return jsonify({"error": "Subtask not found"}), 404
#     return jsonify(subtask)


# @problem_bp.route("/subtasks/<string:task_id>", methods=["DELETE"])
# def delete_subtask(task_id):
#     subtask = g.problem_service.query_subtask(task_id)
#     if subtask is None:
#         return jsonify({"error": "Subtask not found"}), 404
#     subtask_id = g.problem_service.delete_subtask(task_id)
#     return jsonify({"subtask_id": subtask_id})

# @problem_bp.route("/subtasks/<string:task_id>", methods=["PUT"])
# def update_subtask(task_id):
#     subtask = g.problem_service.query_subtask(task_id)
#     if subtask is None:
#         return jsonify({"error": "Subtask not found"}), 404
#     task_name = request.json.get("task_name")
#     points = request.json.get("points")
#     # is_valid = request.json.get("is_valid")
#     subtask_id = g.problem_service.update_subtask(task_id, task_name, points)
#     return jsonify({"Subtask id": subtask_id})

"""
#####
Playbooks
#####
"""

# @problem_bp.route("/<string:problem_id>/playbooks", methods=["POST"])
# def create_playbook(problem_id):
#     playbook_name = request.json.get("playbook_name")
#     playbook_id = g.problem_service.create_playbook(problem_id, playbook_name)
#     return jsonify({"playbook_id": playbook_id})

# @problem_bp.route("/playbooks/<string:playbook_id>", methods=["GET"])
# def query_playbook(playbook_id):
#     playbook = g.problem_service.query_playbook(playbook_id)
#     return jsonify(playbook)

# @problem_bp.route("/playbooks/<string:playbook_id>", methods=["DELETE"])
# def delete_playbook(playbook_id):
#     result = g.problem_service.delete_playbook(playbook_id)
#     return jsonify({"result": result})

# @problem_bp.route("/playbooks/<string:playbook_id>", methods=["PUT"])
# def update_playbook(playbook_id):
#     new_name = request.json.get("new_name")
#     result = g.problem_service.update_playbook(playbook_id, new_name)
    
#     return jsonify({"result": result})