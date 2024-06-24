from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileAllowed

class PublicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(max=300)])
    price = FloatField('Price', validators=[DataRequired()])
    localization = StringField('Localization', validators=[DataRequired(), Length(max=30)])
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Create Publication')
