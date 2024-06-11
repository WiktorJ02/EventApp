from app.models.users import Users
from app.models.publications  import Publications 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.create_pub import PublicationForm
from app.models.publications import Publications


main = Blueprint('main', __name__)


@main.route('/')
def home():
    publications = Publications.query.filter_by(is_visible=True).all()
    
    for pub in publications:
        user = Users.query.get(pub.creating_user_id)
        pub.creating_user_first_name = user.first_name
        pub.creating_user_last_name = user.last_name
    
    return render_template('home.html', publications=publications)

@main.route('/user/<user_id>')
def display_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    user_publications = Publications.query.filter_by(creating_user_id=user_id, is_visible=True).all()
    
    return render_template('user.html', user=user, user_publications=user_publications)

@main.route('/create_publication', methods=['GET', 'POST'])
@login_required
def create_publication():
    form = PublicationForm()
    if form.validate_on_submit():
        new_pub = Publications(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            localization=form.localization.data,
            image=form.image.data,
            creating_user_id=current_user.id
        )
        db.session.add(new_pub)
        db.session.commit()
        flash('Publication created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_publication.html', form=form)


@main.route('/publication/<int:pub_id>')
def publication_details(pub_id):
    publication = Publications.query.get_or_404(pub_id)
    creator = Users.query.get(publication.creating_user_id)
    return render_template('publication_details.html', publication=publication, creator=creator)