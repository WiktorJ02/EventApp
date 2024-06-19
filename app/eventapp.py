from app.models.users import Users
from app.models.publications  import Publications 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.create_pub import PublicationForm
from app.models.publications import Publications
from app.models.ratings import Ratings
from flask_wtf import FlaskForm
from wtforms import SubmitField

main = Blueprint('main', __name__)

# Class for deleting publication
class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

# Publications list
@main.route('/')
def home():
    publications = Publications.query.filter_by(is_visible=True).all()
    
    for pub in publications:
        user = Users.query.get(pub.creating_user_id)
        pub.creating_user_first_name = user.first_name
        pub.creating_user_last_name = user.last_name
    
    return render_template('home.html', publications=publications)

# Create publicataion
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

# Publication details
@main.route('/publication/<int:pub_id>', methods=['GET', 'POST'])
def publication_detail(pub_id):
    publication = Publications.query.get_or_404(pub_id)
    delete_form = DeleteForm()
    ratings = Ratings.query.filter_by(publication_id=pub_id).all()
    creator = Users.query.get(publication.creating_user_id)
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You need to be logged in to rate publications.', 'error')
            return redirect(url_for('main.publication_detail', pub_id=pub_id))
        
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')

        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5.', 'error')
            return redirect(url_for('main.publication_detail', pub_id=pub_id))

        new_rating = Ratings(rating=rating, comment=comment, user_id=current_user.id, publication_id=pub_id)
        db.session.add(new_rating)
        db.session.commit()

        flash('Your rating has been submitted!', 'success')
        return redirect(url_for('main.publication_detail', pub_id=pub_id))

    return render_template('publication_details.html', publication=publication, ratings=ratings, creator=creator, delete_form=delete_form)

# Delete publciations
@main.route('/publication/delete/<int:pub_id>', methods=['POST'])
@login_required
def delete_publication(pub_id):
    publication = Publications.query.get_or_404(pub_id)
    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        if not current_user.is_admin and current_user.id != publication.creating_user_id:
            flash('You do not have permission to delete this publication.', 'error')
            return redirect(url_for('main.publication_detail', pub_id=pub_id))
        
        db.session.delete(publication)
        db.session.commit()
        flash('Publication has been deleted.', 'success')
        return redirect(url_for('main.home'))
    
    flash('Invalid form submission.', 'error')
    return redirect(url_for('main.publication_detail', pub_id=pub_id))