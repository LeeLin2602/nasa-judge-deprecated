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

@app.route("/problems", methods=["GET"])
def query_all_problems():
    problems = problem_service.query_all_problems()
    return jsonify(problems)

@app.route("/problems/<string:problem_id>", methods=["PUT"])
def update_problem(problem_id):
    problem_name = request.json.get("problem_name")
    start_time = request.json.get("start_time")
    deadline = request.json.get("deadline")
    problem_id = problem_service.update_problem(problem_id, problem_name, start_time, deadline)
    return jsonify({"problem_id": problem_id})
