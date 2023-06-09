from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    """Handles the filter feature form"""
    filter_by = StringField(validators=[DataRequired()])
    field = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Filter')

