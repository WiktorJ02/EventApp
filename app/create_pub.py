from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class PublicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    price = FloatField('Price', validators=[DataRequired()])
    localization = StringField('Localization', validators=[DataRequired(),Length(max=30)])
    image = StringField('Image URL', validators=[DataRequired(),Length(max=100)])
    submit = SubmitField('Create Publication')
