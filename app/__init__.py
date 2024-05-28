from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)

    from app.eventapp import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import at as at_blueprint
    app.register_blueprint(at_blueprint)

    return app

main = Blueprint('main', __name__)
authentication = Blueprint('authentication', __name__)

from app import eventapp