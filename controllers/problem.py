from flask import url_for, jsonify, request, g

from app import app
# from service.problem_service import problem_service
from main import problem_service

# check user role at here 
# parse json
"""
#####
for testing
#####
"""
@app.route('/numbers/')
def print_list():
    return jsonify(list(range(5)))

@app.route("/problems", methods=["POST"])
def create_problem():
    problem_id = problem_service.create_problem("New Problem")
    return jsonify({"problem_id": problem_id})

@app.route("/problems/<string:problem_id>", methods=["DELETE"])
def delete_problem(problem_id):
    problem_id = problem_service.delete_problem(problem_id)
    return jsonify({"problem_id": problem_id})

@app.route("/problems/<string:problem_id>", methods=["GET"])
def query_problem(problem_id):
    problem = problem_service.query_problem(problem_id)
    return jsonify(problem)

@app.route("/problems/<string:problem_id>", methods=["PUT"])
def update_problem(problem_id):
    problem_name = request.json.get("problem_name")
    start_time = request.json.get("start_time")
    deadline = request.json.get("deadline")
    problem_id = problem_service.update_problem(problem_id, problem_name, start_time, deadline)
    return jsonify({"problem_id": problem_id})

@app.route("/problems", methods=["GET"])
def query_all_problems():
    problems = problem_service.query_all_problems()
    return jsonify(problems)

@app.route("/problems/<string:problem_id>/subtasks/", methods=["GET"])
def query_all_subtasks(problem_id):
    subtasks = problem_service.query_all_subtasks(problem_id)
    return jsonify(subtasks)

@app.route("/problems/<string:problem_id>/playbooks/", methods=["GET"])
def query_all_playbooks(problem_id):
    playbooks = problem_service.query_all_playbooks(problem_id)
    return jsonify(playbooks)
# subtask
@app.route("/problems/<string:problem_id>/subtasks", methods=["POST"])
def create_subtask(problem_id):
    task_name = request.json.get("task_name")
    points = request.json.get("points")
    subtask_id = problem_service.create_subtask(problem_id, task_name, points)
    return jsonify({"subtask_id": subtask_id})

@app.route("/subtasks/<string:task_id>", methods=["GET"])
def query_subtask(task_id):
    subtask = problem_service.query_subtask(task_id)
    return jsonify(subtask)


@app.route("/subtasks/<string:task_id>", methods=["DELETE"])
def delete_subtask(task_id):
    result = problem_service.delete_subtask(task_id)
    return jsonify({"result": result})

@app.route("/subtasks/<string:task_id>", methods=["PUT"])
def update_subtask(task_id):
    task_name = request.json.get("task_name")
    points = request.json.get("points")
    is_valid = request.json.get("is_valid")
    result = problem_service.update_subtask(task_id, task_name, points, is_valid)
    return jsonify({"result": result})

## playbook
@app.route("/problems/<string:problem_id>/playbooks", methods=["POST"])
def create_playbook(problem_id):
    playbook_name = request.json.get("playbook_name")
    playbook_id = problem_service.create_playbook(problem_id, playbook_name)
    return jsonify({"playbook_id": playbook_id})

@app.route("/playbooks/<string:playbook_id>", methods=["GET"])
def query_playbook(playbook_id):
    playbook = problem_service.query_playbook(playbook_id)
    return jsonify(playbook)

@app.route("/playbooks/<string:playbook_id>", methods=["DELETE"])
def delete_playbook(playbook_id):
    result = problem_service.delete_playbook(playbook_id)
    return jsonify({"result": result})

@app.route("/playbooks/<string:playbook_id>", methods=["PUT"])
def update_playbook(playbook_id):
    new_name = request.json.get("new_name")
    result = problem_service.update_playbook(playbook_id, new_name)
    return jsonify({"result": result})