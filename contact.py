from flask import render_template, redirect, url_for, flash, Blueprint


contact = Blueprint('contact', __name__)



@contact.route('/contact')
def contact():
    return render_template('contact.html')


