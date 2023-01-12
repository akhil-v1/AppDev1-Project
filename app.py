import os
from PIL import Image

from flask import Flask
from flask import request
from flask import render_template, flash, redirect, url_for

from sqlalchemy import or_, desc

from Database.model import *

UPLOAD_FOLDER = '/Users/akhil/Documents/AppDev1-Project/static/uploads'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogLite.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)


@app.before_first_request
def create_all():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        firstname, lastname, email, password, username = request.form['firstname'], request.form[
            'lastname'], request.form['email'], request.form['password'], request.form['username']
        followers_count = 0
        posts_count = 0
        following_count = 0
        error = ""
        # print(firstname, lastname, username, email, password)

        user_data = User.query.filter_by(username=username).first()
        if user_data:
            error = 'Username already exists.'
            return render_template('signup.html', error=error)

        user_data = User.query.filter_by(email=email).first()
        if user_data:
            error = 'Email already registered.'
            return render_template('signup.html', error=error)

        else:
            new_user = User(first_name=firstname,
                            last_name=lastname, username=username, email=email, pwd=password, followers_count=followers_count, following_count=following_count, posts_count=posts_count)
            usr_pth = os.path.join(
                app.config['UPLOAD_FOLDER'], username)
            if not os.path.exists(usr_pth):
                os.makedirs(usr_pth)

            # print(new_user)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id, password = request.form['user_id'], request.form['password']
        error = ""
        # print(user_id, password)

        user_data = db.session.query(User).filter(
            or_(User.email.like(str(user_id)), User.username.like(str(user_id)))).first()
        # print(user_data)

        if user_data:
            if user_data.pwd == password:
                username = user_data.username
                return redirect(f"/dashboard/{username}")
            else:
                error = "Incorrect password"
                return render_template('login.html', error=error)
        else:
            error = "User does not exist"
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')


@app.route('/dashboard/<string:username>', methods=['POST', 'GET'])
def welcome(username):
    if request.method == 'GET':
        posts = Post.query.order_by(desc(Post.timestamp)).all()
        return render_template('dashboard.html', username=username, posts=posts)
    elif request.method == 'POST':
        user_data = User.query.filter_by(username=username).first()
        post_title, post_des, post_img = request.form[
            'post_title'], request.form['post_des'], Image.open(request.files['post_img'])
        print(post_img.filename)

        img_id = f'{username}_{user_data.posts_count + 1}.png'

        post_img_pth = os.path.join(app.config['UPLOAD_FOLDER'], img_id)
        post_img.save(post_img_pth)
        print(post_title, post_des, post_img_pth)

        post_data = Post(name=post_title, caption=post_des, img_id=img_id)
        # print(post_data)
        user_data.posts_count += 1
        db.session.add(post_data)
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('welcome', username=username))


@app.route('/profile/<string:username>', methods=['POST', 'GET'])
def profile(username):
    if request.method == 'GET':
        users = User.query.all()
        user_data = User.query.filter_by(username=username).first()
        print(user_data.followers_count)
        print(user_data.following_count)
        print(user_data.posts_count)
        return render_template('profile.html', username=username, users_data=users, user_data=user_data)
    else:
        return "Working"


@app.route('/edit_post', methods=['POST'])
def edit_post():
    pass

@app.route('/delete_post', methods=['POST'])
def delete_post():
    pass


# @app.route('/create_post', methods=['POST', 'GET'])
# def create_post():
#     if request.method == 'POST':
#         return render_template('welcome.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
