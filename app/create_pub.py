from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed

class PublicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(max=300)])
    price = FloatField('Price', validators=[DataRequired()])
    tickets_number = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1, message="Must be at least 1")])
    localization = StringField('Localization', validators=[DataRequired(), Length(max=30)])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Create Publication')
