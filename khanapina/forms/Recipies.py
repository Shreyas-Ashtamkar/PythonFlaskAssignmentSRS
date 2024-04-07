from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class CreateRecipie(FlaskForm):
    title = StringField('Recipie Name', validators=[DataRequired(), Length(min=2)])
    description  = TextAreaField('Recipie Description', validators=[DataRequired(), Length(min=2)])
    ingredients  = TextAreaField('Recipie Ingredients', validators=[DataRequired(), Length(min=4)])
    instructions = TextAreaField('Recipie Instructions', validators=[DataRequired(), Length(min=4)])
