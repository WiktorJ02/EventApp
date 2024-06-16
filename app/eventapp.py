from app.models.users import Users
from app.models.publications  import Publications 
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.create_pub import PublicationForm
from app.models.publications import Publications
from app.models.ratings import Ratings


main = Blueprint('main', __name__)


@main.route('/')
def home():
    publications = Publications.query.filter_by(is_visible=True).all()
    
    for pub in publications:
        user = Users.query.get(pub.creating_user_id)
        pub.creating_user_first_name = user.first_name
        pub.creating_user_last_name = user.last_name
    
    return render_template('index.html', publications=publications)

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
def publication_detail(pub_id):
    publication = Publications.query.get_or_404(pub_id)
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

    ratings = Ratings.query.filter_by(publication_id=pub_id).all()
    creator = Users.query.get(publication.creating_user_id)
    return render_template('publication_details.html', publication=publication, ratings=ratings, creator=creator)