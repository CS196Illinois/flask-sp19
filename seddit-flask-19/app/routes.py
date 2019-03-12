from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from app.forms import LoginForm, PostForm

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
    form = LoginForm()

    if form.validate_on_submit():
        flash('Welcome back to Seddit, u/{}!'.format(form.username.data))
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

if __name__ == "__main__":
    app.secret_key = Config.SECRET_KEY
    app.run(debug=True)