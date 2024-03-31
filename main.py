from flask import Flask, jsonify, request
from repository import Profile
from sqlalchemy import create_engine
import config
app = Flask(__name__)


connection_string = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PSWD}"
    f"@{config.MYSQL_HOST}/{config.MYSQL_DB}"
)
SQL_ENGINE = create_engine(connection_string)

profile = Profile(SQL_ENGINE)

profile.add_profile()
profile.del_profile(1)


if __name__ == '__main__':
    app.run(debug=True)
