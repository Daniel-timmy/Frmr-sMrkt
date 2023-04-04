from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


# must add mimetype
class ProductForm(FlaskForm):
    """the form class that processes product input from users"""
    images = FileField(label='Product image:',
                       validators=[DataRequired(), FileRequired(),
                                   FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    farm_name = StringField(label='Farm name:')
    state = StringField(label='State:')
    product_name = StringField(label='Product name:', validators=[DataRequired()])
    contact = StringField(label='Contact(WhatsApp):')
    submit = SubmitField(label='Submit')
