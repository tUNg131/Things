from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, EqualTo, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matkhau'

class signUpForm(FlaskForm):
    username = StringField('Username', [InputRequired()], render_kw={"placeholder": "Username"})
    # pip install email_validator
    email = StringField('Email', [InputRequired(message='You must have username'), validators.Email()], render_kw={"placeholder": "Email"})
    address = StringField('Address', [InputRequired(message='You must have address')], render_kw={"placeholder": "Address"})
    password = PasswordField('Password', [InputRequired(message='You must have password')], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', [InputRequired(), EqualTo('password', message='Password must match')], render_kw={"placeholder": "Repeat Password"})

@app.route('/', methods=['GET', 'POST'])
def form():
    form = signUpForm()

    if form.validate_on_submit():
        return 'You have signed up'

    return render_template('Sign_Up.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)