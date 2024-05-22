from app.routes import main
from app import db
from app.models.users import Users
from app.models.publications  import Publications 
from flask import render_template

@main.route('/')
def home():
    publications = Publications.query.all()
    
    
    for pub in publications:
        user = Users.query.get(pub.creating_user_id)
        pub.creating_user_first_name = user.first_name
        pub.creating_user_last_name = user.last_name
    
    return render_template('home.html', publications = publications)