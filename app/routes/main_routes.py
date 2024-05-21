from flask import Blueprint

from . import main

@main.route('/')
def home():
    return "Welcome to the Home Page"

@main.route('/about')
def about():
    return "About Page"