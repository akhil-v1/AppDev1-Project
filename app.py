import os
from PIL import Image

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for

from sqlalchemy import or_

from Database.model import *

# path for saving user post images
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
        # confirm_pwd = request.form['confirm_password']

        # if password != confirm_pwd:
        #     error = 'Passwords do not match'
        #     return render_template('signup.html', error=error)

        # if len(password) < 8:
        #     error='Password should contain 8 or more characters'
        #     return render_template('signup.html', error=error)

        # chars = ['!', '@']
        # check = False
        # for char in chars:
        #     if char in password:
        #         check = True
        #         break
        # if not check:
        #     error = 'Password must contain spl chr'
        #     return render_template('signup.html', error=error)

        user_data = User.query.filter_by(username=username).first()
        if user_data:
            error = 'Username already exists.'
            return render_template('signup.html', error=error)

        user_data = User.query.filter_by(email=email).first()
        if user_data:
            error = 'Email already registered.'
            return render_template('signup.html', error=error)

        new_user = User(first_name=firstname, last_name=lastname, username=username,
                        email=email, pwd=password, followers_count=0, following_count=0, posts_count=0)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('signup.html', error='')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id, password = request.form['user_id'], request.form['password']

        user_data = db.session.query(User).filter(
            or_(User.email.like(str(user_id)), User.username.like(str(user_id)))).first()

        if user_data:
            if password == user_data.pwd:
                username = user_data.username
                return redirect(f"/{username}")
            else:
                error = "Incorrect password"
                return render_template('login.html', error=error)
        else:
            error = "User does not exist"
            return render_template('login.html', error=error)

    else:
        return render_template('login.html', error='')


@app.route('/<string:current_user>', methods=['POST', 'GET'])
def dashboard(current_user):
    if request.method == 'GET':
        current_user_data = User.query.filter_by(username=current_user).first()
        posts = []
        if current_user_data.following:
            followedIDs = current_user_data.following.split('_')

            followingPosts = []
            for followedID in followedIDs:
                followingPosts.append(UserPosts.query.with_entities(
                    UserPosts.postID).filter(UserPosts.userID == followedID).all())
            # followingPosts = [UserPosts.query.with_entities(UserPosts.postID).filter(UserPosts.userID == followedID).all() for followedID in followedIDs]

            for userPosts in followingPosts:
                for postID in userPosts:
                    posts.append(Post.query.filter_by(id=postID[0]).first())

        return render_template('dashboard.html', current_user=current_user, posts=sorted(posts, key=lambda x: x.timestamp, reverse=True))
        # return render_template('dashboard.html', current_user=current_user, posts=reversed(posts))
    elif request.method == 'POST':
        current_user_data = User.query.filter_by(username=current_user).first()

        post_title, post_des = request.form['post_title'], request.form['post_des']
        img_id = f'{current_user}_{current_user_data.posts_count + 1}'
        new_post = Post(creator=current_user_data.username,
                        name=post_title, caption=post_des, contains_img=False, img_id=img_id)

        if request.files['post_img']:
            post_img = Image.open(request.files['post_img'])

            post_img_pth = os.path.join(
                app.config['UPLOAD_FOLDER'], img_id+'.png')
            post_img.save(post_img_pth)

            new_post.contains_img = True

        current_user_data.posts_count += 1
        current_user_data.posts.append(new_post)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard', current_user=current_user))


@app.route('/<string:current_user>/search', methods=['POST'])
def search(current_user):
    if request.form['user_query']:
        return redirect(url_for('search_user', current_user=current_user, user_query=request.form['user_query']))
    else:
        return redirect(url_for('search_user', current_user=current_user, user_query=' '))


@app.route('/<string:current_user>/search?name=<string:user_query>', methods=['GET'])
def search_user(current_user, user_query):
    user_query_data = db.session.query(User).filter(or_(User.email.like('%' + str(user_query.split('@')) + '%'), User.username.like(
        f'%{user_query}%'), User.first_name.like(f'%{user_query}%'), User.last_name.like('%' + str(user_query) + '%'))).all()
    return render_template('result.html', user_query=user_query, user_query_data=user_query_data, current_user=current_user, isData=True if user_query_data else False)


@app.route('/<string:current_user>/<string:user_profile>/profile', methods=['GET'])
def user_profile(current_user, user_profile):
    isFollowed = False
    current_user_data = User.query.filter_by(username=current_user).first()
    user_profile_data = User.query.filter_by(username=user_profile).first()

    user_profile_postIDs = UserPosts.query.with_entities(
        UserPosts.postID).filter(UserPosts.userID == user_profile_data.id).all()

    user_profile_posts = []
    for user_profile_postID in user_profile_postIDs:
        user_profile_posts.append(Post.query.filter_by(
            id=user_profile_postID[0]).first())
    # user_profile_posts = [Post.query.filter_by(id=user_profile_postID[0]).first() for user_profile_postID in user_profile_postIDs]

    users_data = User.query.all()

    followers = user_profile_data.followers
    if followers:
        followers = followers.split('_')
        if str(current_user_data.id) in followers:
            isFollowed = True

    return render_template('pub_profile.html', current_user=current_user, users_data=users_data, user_profile_data=user_profile_data, user_profile_posts=sorted(user_profile_posts, key=lambda x: x.timestamp, reverse=True), isFollowed=isFollowed)


@app.route('/<string:current_user>/account', methods=['GET'])
def my_profile(current_user):
    current_user_data = User.query.filter_by(username=current_user).first()

    users_data = User.query.all()
    my_postIDs = UserPosts.query.with_entities(
        UserPosts.postID).filter(UserPosts.userID == current_user_data.id).all()

    my_posts = []
    for my_postID in my_postIDs:
        my_posts.append(Post.query.filter_by(id=my_postID[0]).first())
    # my_posts = [Post.query.filter_by(id=my_postID[0]).first() for my_postID in my_postIDs]

    return render_template('pvt_profile.html', current_user_data=current_user_data, users_data=users_data, my_posts=sorted(my_posts, key=lambda x: x.timestamp, reverse=True))


@app.route('/<string:current_user>/<string:user_profile>/follow', methods=['GET'])
def follow(current_user, user_profile):
    current_user_data = User.query.filter_by(username=current_user).first()
    user_profile_data = User.query.filter_by(username=user_profile).first()

    if user_profile_data.followers is None:
        user_profile_data.followers = str(current_user_data.id)
    else:
        user_profile_data.followers += '_' + str(current_user_data.id)

    if current_user_data.following is None:
        current_user_data.following = str(user_profile_data.id)
    else:
        current_user_data.following += '_' + str(user_profile_data.id)

    current_user_data.following_count += 1
    user_profile_data.followers_count += 1
    db.session.commit()
    return redirect(url_for('user_profile', current_user=current_user, user_profile=user_profile))


@app.route('/<string:current_user>/<string:user_profile>/unfollow', methods=['GET'])
def unfollow(current_user, user_profile):
    current_user_data = User.query.filter_by(username=current_user).first()
    user_profile_data = User.query.filter_by(username=user_profile).first()

    temp = user_profile_data.followers.split('_')
    temp.remove(str(current_user_data.id))
    if temp:
        user_profile_data.followers = '_'.join(temp)
    else:
        user_profile_data.followers = None

    temp = current_user_data.following.split('_')
    temp.remove(str(user_profile_data.id))
    if temp:
        current_user_data.following = '_'.join(temp)
    else:
        current_user_data.following = None

    current_user_data.following_count -= 1
    user_profile_data.followers_count -= 1
    db.session.commit()
    return redirect(url_for('user_profile', current_user=current_user, user_profile=user_profile))


@app.route('/<string:current_user>/<int:post_id>/edit_post', methods=['GET', 'POST'])
def edit_post(current_user, post_id):
    if request.method == 'GET':
        current_user_data = User.query.filter_by(username=current_user).first()
        post_data = Post.query.filter_by(id=post_id).first()
        return render_template('edit_post.html', current_user_data=current_user_data, post_data=post_data)
    else:
        post_data = Post.query.filter_by(id=post_id).first()

        post_data.name = request.form['post_title']
        post_data.caption = request.form['post_des']

        temp_id = post_data.img_id
        if post_data.contains_img:
            os.remove(os.path.join(
                app.config['UPLOAD_FOLDER'], temp_id+'.png'))
            post_data.contains_img = False

        if request.files['post_img']:
            post_img = Image.open(request.files['post_img'])

            post_img_pth = os.path.join(
                app.config['UPLOAD_FOLDER'], temp_id+'.png')
            post_img.save(post_img_pth)

            post_data.img_id = temp_id
            post_data.contains_img = True

        db.session.commit()
        return redirect(url_for('my_profile', current_user=current_user, post_id=post_id))


@app.route('/<string:current_user>/<int:post_id>/delete_post', methods=['GET'])
def delete_post(current_user, post_id):
    user_data = User.query.filter_by(username=current_user).first()
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    user_data.posts_count -= 1
    db.session.commit()
    return redirect(url_for('my_profile', current_user=current_user))


if __name__ == '__main__':
    app.run(debug=True)
