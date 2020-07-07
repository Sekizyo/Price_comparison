from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Search_item(FlaskForm):
    item = StringField("Search", validators=[DataRequired()])
    sort_by = SelectField("Sort_by", validators=[DataRequired()], choices=[('price_low', 'Price low'), ('price_high', 'Price high'), ('name_low', 'Name low'), ('name_high', 'Name high')])
    submit = SubmitField('Potwierdz')

class Query_items(FlaskForm):
    query = SelectField("Query", validators=[DataRequired()], choices=[('all', "All"), ('x_kom', 'X-kom'), ('morele', 'Morele'), ('media_expert', 'Media expert')])
    submit = SubmitField('Potwierdz')

class Spec_item(FlaskForm):
    url = StringField("Url", validators=[DataRequired()])
    choice = SelectField("Choice", validators=[DataRequired()], choices=[('all', "All"), ('x_kom', 'X-kom'), ('morele', 'Morele'), ('media_expert', 'Media expert')])
    submit = SubmitField('Potwierdz')

class Spec_add(FlaskForm):
    url = StringField("Url", validators=[DataRequired()])
    submit = SubmitField('Potwierdz')

class Spec_del(FlaskForm):
    id = StringField("Spec id", validators=[DataRequired()])
    submit = SubmitField('Potwierdz')
    
