import logging
from sqlalchemy import create_engine
from flask import Flask
from authlib.integrations.flask_client import OAuth

import config
from repository import users, Profiles, problems
from service import AuthService, problem_service
from models import wg
from flask import url_for, jsonify, request, g
from app import app

connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PSWD}"
    f"@{config.MYSQL_HOST}/{config.MYSQL_DB}"
)

SQL_ENGINE = create_engine(connection_string)
profiles = Profiles(SQL_ENGINE)

print(wg.generate_wireguard_config(profiles.add_profile()))
print("\n\n\n\n\n\n\n")


users = users.Users(SQL_ENGINE)
auth_service = AuthService(logging, config.JWT_SECRET, users)
problems = problems.Problems(SQL_ENGINE)
problem_service = problem_service(logging, config.JWT_SECRET, problems)
from controllers import auth, problem # pylint: disable=wrong-import-position, unused-import, cyclic-import

if __name__ == "__main__":
    app.run(debug=True)
    
