from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList
from wtforms.validators import DataRequired, Length

class CreateRecipie(FlaskForm):
    title = StringField('Recipie Name', validators=[DataRequired(), Length(min=2)])
    description  = TextAreaField('Recipie Description', validators=[DataRequired(), Length(min=2)])
    ingredients  = FieldList(StringField('Ingredient', validators=[DataRequired(), Length(min=4)]), label="Recipie Ingredients", min_entries=1)
    instructions = TextAreaField('Recipie Instructions', validators=[DataRequired(), Length(min=4)])
    category = StringField('Recipie Category', default="Lunch")
