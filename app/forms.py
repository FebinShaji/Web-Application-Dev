#These first 3 lines import the necessary librariess
#in order to create the forms below
from flask_wtf import Form
from wtforms import TextField, TextAreaField, DateField, PasswordField
from wtforms.validators import DataRequired

#Form that allows the user to sign in
class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

#Form that allows the user to register
class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    first_name = TextField('first_name', validators=[DataRequired()])
    last_name = TextField('last_name', validators=[DataRequired()])
    number = TextField('number', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])

#Form that allows the user to change their password
class PasswordForm(Form):
    password_change1 = PasswordField('password_change1', validators=[DataRequired()])
    password_change2 = PasswordField('password_change2', validators=[DataRequired()])

#Form that allows the user to add a book
class AddBookForm(Form):
    title = TextField('title', validators=[DataRequired()])
    author = TextField('author', validators=[DataRequired()])

#Form that allows the user to add a review
class AddReviewForm(Form):
    title = TextField('title', validators=[DataRequired()])
    book_name = TextField('book_name', validators=[DataRequired()])
    author = TextField('author', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
