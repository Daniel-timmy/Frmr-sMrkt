from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectMultipleField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from models.registered_farm import Business
from models.customers import Customers


class BusinessForm(FlaskForm):
    """Farm registration form"""

    def validate_email(self, input_email):
        """it checks if a user with a particular email exist"""
        from models import storage
        user = storage.get(attr=input_email, cls=Business)
        if user:
            raise ValidationError('User with e-mail already exist')

    def validate_farm_name(self, input_farm_name):
        """it checks if a user with a particular farm name exist"""
        from models import storage
        user = storage.get(attr=input_farm_name, cls=Business)
        if user:
            raise ValidationError('Farm name already exist')

    business_name = StringField(label='Business name:', validators=[DataRequired()])
    email = EmailField(label='E-mail', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password1 = PasswordField(label='Confirm password:', validators=[EqualTo('password'), DataRequired()])
    contact = StringField(label='Contact(WhatsApp):', validators=[DataRequired()])
    location = StringField(label='Location:', validators=[DataRequired()])
    company_logo = FileField(label='Farm logo:',
                             validators=[DataRequired(), FileRequired(),
                                         FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    about = StringField(label='About Farm')
    submit = SubmitField(label='Save profile')


class CustomersForm(FlaskForm):
    """Customer registration class"""

    def validate_email(self, input_email):
        """it checks if a user with a particular email exist"""
        from models import storage
        customer = storage.get(attr=input_email, cls=Customers)
        if customer:
            raise ValidationError('User with e-mail already exist')

    def validate_username(self, input_username):
        """it checks if a user with a particular username exist"""
        from models import storage
        customer = storage.get(attr=input_username, cls=Customers)
        if customer:
            raise ValidationError('Username already exist')

    username = StringField(label='Username:', validators=[DataRequired()])
    email = EmailField(label='E-mail', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    password1 = PasswordField(label='Confirm password:', validators=[EqualTo('password'), DataRequired()])
    contact = StringField(label='Contact(WhatsApp):', validators=[DataRequired()])
    profile_pic = FileField(label='Farm logo:',
                            validators=[DataRequired(), FileRequired(),
                                        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    submit = SubmitField(label='Save profile')
