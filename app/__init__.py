from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'login.user_login'
login_manager.session_protection = 'strong'
csrf = CSRFProtect()


def create_app(config_name):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)


    from app.eventapp import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import at as at_blueprint
    app.register_blueprint(at_blueprint)
    
    from app.login import login as login_blueprint
    app.register_blueprint(login_blueprint)
    
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from app.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app


    
