from PIL import Image
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.users import Users
from app.models.publications import Publications
from app import db
from app.create_pub import PublicationForm
from app.models.ratings import Ratings
from flask_wtf import FlaskForm
from wtforms import SubmitField
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
    
# Resizing images function
def resize_image(image_path, output_size=(300, 300)):
    with Image.open(image_path) as img:
        img_ratio = img.width / img.height
        target_ratio = output_size[0] / output_size[1]
        
        if img_ratio > target_ratio:
            new_width = int(target_ratio * img.height)
            left = (img.width - new_width) // 2
            right = left + new_width
            img = img.crop((left, 0, right, img.height))
        else:
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            bottom = top + new_height
            img = img.crop((0, top, img.width, bottom))
        
        img = img.resize(output_size, Image.LANCZOS)
        img.save(image_path)    

@main.route('/')
def home():
    publications = Publications.query.filter_by(is_visible=True).order_by(Publications.creation_date.desc()).all()
    for pub in publications:
        user = Users.query.get(pub.creating_user_id)
        pub.creating_user_first_name = user.first_name
        pub.creating_user_last_name = user.last_name
    return render_template('home.html', publications=publications)

@main.route('/create_publication', methods=['GET', 'POST'])
@login_required
def create_publication():
    form = PublicationForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(file_path)
            resize_image(file_path) 
        
        new_pub = Publications(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            localization=form.localization.data,
            image=filename,
            creating_user_id=current_user.id
        )
        db.session.add(new_pub)
        db.session.commit()
        flash('Publication created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_publication.html', form=form)


@main.route('/publication/<int:pub_id>', methods=['GET', 'POST'])
def publication_detail(pub_id):
    publication = Publications.query.get_or_404(pub_id)
    delete_form = DeleteForm()
    form = PublicationForm(obj=publication)
  
    ratings = Ratings.query.filter_by(publication_id=pub_id).all()
    creator = Users.query.get(publication.creating_user_id)
    return render_template('publication_details.html', publication=publication, ratings=ratings, creator=creator, delete_form=delete_form, form=form)

@main.route('/update_publication/<int:pub_id>', methods=['GET', 'POST'])
@login_required
def update_publication(pub_id):
    publication = Publications.query.get_or_404(pub_id)
    form = PublicationForm(obj=publication)
    
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            
            # Save the file
            form.image.data.save(file_path)
            
            # Open the image for resizing
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.LANCZOS)  # Resize to 300x300 pixels
            image.save(file_path)  # Save the resized image
            
            publication.image = filename
        
        # Update other fields
        publication.name = form.name.data
        publication.description = form.description.data
        publication.price = form.price.data
        publication.localization = form.localization.data

        db.session.commit()
        flash('Publication updated successfully!', 'success')
        return redirect(url_for('main.publication_detail', pub_id=pub_id))
    
    return render_template('update_publication.html', form=form, publication=publication)

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

