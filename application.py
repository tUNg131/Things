from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'application'
users = {'admin': 'admin'}

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    # pip install email_validator
    email = StringField('Email', validators=[InputRequired(message='You must have username'), Email()])
    address = StringField('Address', validators=[InputRequired(message='You must have address')])
    password = PasswordField('Password', validators=[InputRequired(message='You must have password')])
    confirm = PasswordField('RepeatPassword', validators=[InputRequired(), EqualTo('password', message='Password must match')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class User():
    class Attribute():
        def __init__(self):
            self.data = None
            self.validation = None

    def __init__(self):
        self.username = self.Attribute()
        self.password = self.Attribute()

    def validate(self):
        password = users.get(self.username.data, None)
        if password is not None:
            # username exists
            self.username.validation = True
            if password == self.password.data:
                self.password.validation = True
            else:
                self.password.validation = False
        else:
            # username doesn't exists
            self.username.validation = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        user.username.data = form.username.data
        user.password.data = form.password.data
        user.validate()
        if user.password.validation and user.username.validation:
            return redirect(url_for('success'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        return 'OK!'
    return render_template('signup.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
