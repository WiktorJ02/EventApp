from app import db, login_manager
import pytz
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

# Model of Users table
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)  # Increase length for hashed password
    email = db.Column(db.String(60), nullable=False, unique=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    last_login = db.Column(db.DateTime, nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    created_publications = db.relationship('Publications', backref='creator', lazy=True, foreign_keys='Publications.creating_user_id')
    
    def __init__(self, login, password, email, first_name, last_name, birth_date):
        self.login = login
        self.set_password(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
        
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    
    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True 
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
