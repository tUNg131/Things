<<<<<<< HEAD
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, EqualTo, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matkhau'

class signUpForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    # pip install email_validator
    email = StringField('Email', [InputRequired(message='You must have username'), validators.Email()])
    address = StringField('Address', [InputRequired(message='You must have address')])
    password = PasswordField('Password', [InputRequired(message='You must have password')])
    confirm = PasswordField('RepeatPassword', [InputRequired(), EqualTo('password', message='Password must match')])

@app.route('/', methods=['GET', 'POST'])
def form():
    form = signUpForm()

    if form.validate_on_submit():
        return 'You have signed up'

    return render_template('Sign_Up.html', form=form)

if __name__ == '__main__':
=======
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, EqualTo, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matkhau'

class loginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    # pip install email_validator
    email = StringField('Email', [InputRequired(message='You must have username'), validators.Email()])
    address = StringField('Address', [InputRequired(message='You must have address')])
    password = PasswordField('Password', [InputRequired(message='You must have password')])
    confirm = PasswordField('RepeatPassword', [InputRequired(), EqualTo('password', message='Password must match')])

@app.route('/', methods=['GET', 'POST'])
def form():
    form = loginForm()

    if form.validate_on_submit():
        return 'You have signed up'

    return render_template('Sign_Up.html', form=form)

if __name__ == '__main__':
>>>>>>> 71d86bcaffdd7227fb155f655428a0c674988ecf
    app.run(debug=True)