from flask import Flask, render_template
import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import psycopg2


app = Flask(__name__)

app.config.update(
    SECRET_KEY='admin',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin@localhost/event_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(24), nullable = False)
    password = db.Column(db.String(32), nullable = False)
    first_name = db.Column(db.String(24), nullable = False)
    last_name = db.Column(db.String(24), nullable = False)
    birth_date = db.Column(db.Date, nullable = False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    
    publications = db.relationship('Publications', backref='creator', lazy=True)
    
    
    def __init__(self, login, password, first_name, last_name, birth_date):
        
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        
    def __repr__(self) -> str:
        return 'The id is {}, login {}, name {} {}, date of birth {} and creation date {}'.format(self.id, self.login, self.first_name, self.last_name, self.birth_date, self.creation_date)
    
    
class Publications(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    price = db.Column(db.Float, nullable = False)
    creating_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    accepting_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = True)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Warsaw')))
    image = db.Column(db.String(100))
    is_visible = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, description, price, creating_user_id, image):\
        
        self.name = name
        self.description = description
        self.price = price
        self.creating_user_id = creating_user_id
        self.image = image
        
    def __repr__(self) -> str:
        return 'The id is {}, name {}, description {}, price {} and creation date {}'.format(self.id, self.name, self.description, self.price, self.creation_date)
    

if __name__ == '__main__':
    app.run(debug=True)