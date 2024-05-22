from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.routes.main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
