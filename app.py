from flask import Flask, render_template, redirect, url_for, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Email

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'application'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://LeXuanTung@localhost:5432/things1'
# postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rvgrjnphlwzvjd:fefede7bb2b893a43460c53ac701842ac969b1066d908d9b8f1639ec6e808d54@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d8svuqp19g214c'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class SignUpForm(FlaskForm):
    username = StringField('Username', [InputRequired()], render_kw={"placeholder": "Username"})
    # pip install email_validator
    email = StringField('Email', [InputRequired(message='You must have username'),
                                    Email()], render_kw={"placeholder": "Email"})
    address = StringField('Address', [InputRequired(message='You must have address')], render_kw={"placeholder": "Address"})
    password = PasswordField('Password', [InputRequired(message='You must have password')], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', [InputRequired(),
                                EqualTo('password', message='Password must match')], render_kw={"placeholder": "Repeat Password"})

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', next=request.endpoint))

def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)

@app.route('/')
def landing():
    return render_template('landing_page.html')

@app.route('/homepage')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data,
                                 User.password == form.password.data).first() # need to do the hash password
        if user:
                login_user(user)
                return redirect_dest(fallback=url_for('index'))
        flash('Wrong username or password!')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(User.username == form.username.data,
                                     User.password == form.password.data,
                                     User.email == form.email.data)).first()
        if not user:
            user = User(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            # todo a error catch here if insertion is not successful
            login_user(user)
            return redirect_dest(fallback=url_for('index'))
        else:
            flash(f'User {user.username} has already existed!')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
