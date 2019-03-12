from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from app.forms import LoginForm, PostForm
from flask_login import current_user, login_user, LoginManager, logout_user
from app.models import User
from app import db

app = Flask(__name__)
app.config.from_object(Config)

user = {"username" : "TestUser1"}
posts = [
        {
            "postnumber" : "0",
            "title" : "This is my first post to Seddit!",
            "body" : "Hi my name is TestUser1 and I am new to Seddit",
            "subseddit" : "r/home",
            "author" : {"username" : "u/TestUser1"}
        },
        {
            "postnumber" : "1",
            "title" : "This is my second post",
            "body" : "Hi my name is TestUser2 and I am not new to Seddit anymore!",
            "subseddit" : "r/home",
            "author" : {"username" : "u/TestUser1"}
        }
        ]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Welcome to Seddit! Please log in with your new credentials')
            return redirect(url_for('login'))

        if not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            flash('Welcome back to Seddit!')

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        flash('Post {} was posted to Home'.format(
            form.title.data))
        return redirect(url_for('index'))
    return render_template('newpost.html', title='Post', form=form)

@app.route('/post/<postnumber>')
def post(postnumber):
    return render_template('postpage.html', post=posts[int(postnumber)])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = Config.SECRET_KEY

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    db.init_app(app)

    app.run(debug=True)