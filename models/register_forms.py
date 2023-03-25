from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectMultipleField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from models.loggedusers import LoggedUsers
from models.customers import Customers


class ProfileForm(FlaskForm):
    """Farm registration form"""

    def validate_email(self, input_email):
        """it checks if a user with a particular email exist"""
        from models import storage
        user = storage.get(attr=input_email, cls=LoggedUsers)
        if user:
            raise ValidationError('User with e-mail already exist')

    def validate_farm_name(self, input_farm_name):
        """it checks if a user with a particular farm name exist"""
        from models import storage
        user = storage.get(attr=input_farm_name, cls=LoggedUsers)
        if user:
            raise ValidationError('Farm name already exist')

    firstname = StringField(label='First name:', validators=[DataRequired()])
    lastname = StringField(label='Last name:', validators=[DataRequired()])
    email = EmailField(label='E-mail', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password1 = PasswordField(label='Confirm password:', validators=[EqualTo('password'), DataRequired()])
    contact = StringField(label='Contact(WhatsApp):', validators=[DataRequired()])
    farm_name = StringField(label='Farm name:', validators=[DataRequired()])
    state = StringField(label='Location:', validators=[DataRequired()])
    profile_picture = FileField(label='Farm logo:',
                                validators=[DataRequired(), FileRequired(),
                                            FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    about = StringField(label='About Farm')
    product_base = SelectMultipleField(label='Product base(Plant, Meat):', choices=[('value1', 'Option 1'), ('value2', 'Option 2')],
                                       validators=[DataRequired()])
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

