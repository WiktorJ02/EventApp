from app import db
import pytz
from datetime import datetime

# Model of Users table
class Users(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(24), nullable = False)
    password = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(32), nullable = False)
    first_name = db.Column(db.String(24), nullable = False)
    last_name = db.Column(db.String(24), nullable = False)
    birth_date = db.Column(db.Date, nullable = False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    
# Relationship
    publications = db.relationship('Publications', backref='creator', lazy=True)
    
    
    def __init__(self, login, password, first_name, last_name, birth_date):
        
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        
    def __repr__(self) -> str:
        return 'The id is {}, login {}, name {} {}, date of birth {} and creation date {}'.format(self.id, self.login, self.first_name, self.last_name, self.birth_date, self.creation_date)