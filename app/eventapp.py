from app import main
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


@main.route('/users/<user_id>')
def display_user(user_id):
        
    user = Users.query.filter_by(id = user_id).first()
    user_publications = Publications.query.filter_by(creating_user_id = user_id).all()
        
    return render_template('user.html', user = user, user_publications = user_publications)