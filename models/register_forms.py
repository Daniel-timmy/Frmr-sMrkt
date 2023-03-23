from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectMultipleField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from models.loggedusers import LoggedUsers
from models.customers import Customers


class ProfileForm(FlaskForm):

    def validate_email(self, input_email):
        user = LoggedUsers.query.filter_by(email=input_email.data).first()
        if user:
            raise ValidationError('User with e-mail already exist')

    def validate_farm_name(self, input_farm_name):
        user = LoggedUsers.query.filter_by(email=input_farm_name.data).first()
        if user:
            raise ValidationError('Farm name already exist')

    firstname = StringField(label='First name:', validators=[DataRequired()])
    lastname = StringField(label='Last name:', validators=[DataRequired()])
    email = EmailField(label='E-mail', validators=[DataRequired()])
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
    def validate_email(self, input_email):
        customer = Customers.query.filter_by(email=input_email.data).first()
        if customer:
            raise ValidationError('User with e-mail already exist')

    def validate_username(self, input_email):
        customer = Customers.query.filter_by(email=input_email.data).first()
        if customer:
            raise ValidationError('Username already exist')

    username = StringField(label='First name:', validators=[DataRequired()])
    email = EmailField(label='E-mail', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password1 = PasswordField(label='Confirm password:', validators=[EqualTo('password'), DataRequired()])
    contact = StringField(label='Contact(WhatsApp):', validators=[DataRequired()])
    profile_picture = FileField(label='Farm logo:',
                                validators=[DataRequired(), FileRequired(),
                                            FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    submit = SubmitField(label='Save profile')

