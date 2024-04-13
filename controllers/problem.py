from flask import url_for, jsonify, request, g

from main import app
from service import ProblemService

# check user role at here 
# parse json

@app.route("/create_problem", methods=["POST"])
def create_problem(problem_name, start_time, deadline):
    problem_id = ProblemService.create_problem(problem_name, start_time, deadline)
    return jsonify({"problem_id": problem_id})

@app.route("/delete_problem", method=["DELETE"])
def delete_problem():
    problem_name = request.json.get("problem_name")
    problem_name = ProblemService.delete_problem(problem_name)
    return jsonify({"problem_name": problem_name})

@app.route("/query_problem", method=["GET"])
def query_problem():
    problem_name = request.json.get("problem_name")
    problem = ProblemService.query_problem(problem_name)
    return jsonify(problem)

@app.route("/query_all_problems", method=["GET"])
def query_all_problems():
    problems = ProblemService.query_all_problems()
    return jsonify(problems)

@app.route("/update_problem", method=["PUT"])
def update_problem():
    problem_id = request.json.get("problem_id")
    problem_name = request.json.get("problem_name")
    start_time = request.json.get("start_time")
    deadline = request.json.get("deadline")
    problem_id = ProblemService.update_problem(problem_id, problem_name, start_time, deadline)
    return jsonify({"problem_id": problem_id})