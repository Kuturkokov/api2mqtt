from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, realpath, join
import utils.resources as resources
from config import logger, log_cleaner, variables
from utils.run_verify import check_in


api = Flask(__name__)
PROJECT_ROOT = dirname(realpath(__file__))
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(PROJECT_ROOT, 'data', 'users.db')
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(api)


if __name__ == "__main__":
    logger.info("****** APP Start ******")
    log_cleaner()
    from waitress import serve
    serve(resources.api, _quiet=True, host='0.0.0.0', port=8009)

