from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, RadioField, \
    SelectField, FileField, PasswordField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Regexp, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

photos = UploadSet('photos', IMAGES)


class ContactForm(FlaskForm):
    name = StringField('Full Name *', validators=[InputRequired(), Length(4, 64),
                                                  Regexp('^[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*$', 0,
                                                         'Your name can only contain letters, dots, hyohens, single quotes or spaces')])
    email = EmailField('Email *', validators=[InputRequired(), Email()])
    message = TextAreaField('Message *', validators=[InputRequired()], render_kw={'rows': 10})
    submit = SubmitField('Send Message')


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class NewFriendForm(FlaskForm):
    name = StringField('Name *', validators=[InputRequired(), Length(4, 64),
                                             Regexp('^[A-Za-z]+((s)?((\'|-|.)?([A-Za-z])+))*$', 0,
                                                    'Your name can contain dots, hyphens, single quotes or spaces')])
    phonenumber = StringField('Phone number', validators=[Regexp('\D?(\d{0,3}?)\D{0,2}(\d{3})?\D{0,2}(\d{3})\D?(\d{4})$', 0,
                                                                 'You should enter a valid phone number of 10 digits')])
    age = IntegerField('Age', validators=[NumberRange(1, 90)])
    # checkbox_group = MultiCheckboxField('Country', validators=[InputRequired()],
    #                                     choices=[('c1', 'Swimming'), ('c2', 'Sports'), ('c3', 'Checkbox 3')],
    #                                     render_kw={'required': True})
    radio_group = RadioField('Gender *', validators=[InputRequired()],
                             choices=[('r1', 'Male'), ('r2', 'Female')],
                             render_kw={'required': True})
    select = SelectField('Social accounts *', validators=[InputRequired()],
                         choices=[('o1', 'Facebook'), ('o2', 'Twitter'), ('o3', 'Instagram')])
    accounts = StringField('Account ID *', validators=[InputRequired(), Length(4, 64),
                                            Regexp('^@?([a-zA-Z0-9_]){1,15}$', 0,
                                                'Please enter a valid social media account! I will follow you!')])
    photo = FileField('Wanna upload your photo?', validators=[FileAllowed(photos, 'Images only!')])
    description = TextAreaField('Description *', validators=[InputRequired()], render_kw={'rows': 10})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
