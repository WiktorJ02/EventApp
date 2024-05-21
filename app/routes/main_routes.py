from app.routes import main
from app import db
from app.models.users import Users
from app.models.publications  import Publications 
from flask import render_template

@main.route('/')
def home():
    return "Welcome to the Home Page"

@main.route('/about')
def about():
    return "About Page"