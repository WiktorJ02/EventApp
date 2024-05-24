class Config:
    SECRET_KEY = 'admin'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/event_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': Config
}