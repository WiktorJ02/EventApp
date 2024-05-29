from app import db, login_manager
import pytz
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


bcrypt = Bcrypt()

# Model of Users table
class Users(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(32), nullable = False, unique = True)
    password = db.Column(db.String(60), nullable = False) # length is 60, because hashed password has this length
    email = db.Column(db.String(60), nullable = False, unique = True)
    first_name = db.Column(db.String(32), nullable = False)
    last_name = db.Column(db.String(32), nullable = False)
    birth_date = db.Column(db.Date, nullable = False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    last_login = db.Column(db.DateTime, nullable=True)
    
# Relationship
    created_publications = db.relationship('Publications', backref='creator', lazy=True, foreign_keys='Publications.creating_user_id')
    accepted_publications = db.relationship('Publications', backref='accepter', lazy=True, foreign_keys='Publications.accepting_user_id')
    
    
    def __init__(self, login, password, email, first_name, last_name, birth_date):
        
        self.login = login
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        
    
    def check_password(self, password):
        result = bcrypt.check_password_hash(self.password, password)
        
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))