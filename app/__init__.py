from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'login.user_login'
login_manager.session_protection = 'strong'

def create_app(config_name):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from app.eventapp import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import at as at_blueprint
    app.register_blueprint(at_blueprint)
    
    from app.login import signin as singin_blueprint
    app.register_blueprint(singin_blueprint)

    return app

main = Blueprint('main', __name__)
authentication = Blueprint('authentication', __name__)
signin = Blueprint('login', __name__)

from app import eventapp, auth, login