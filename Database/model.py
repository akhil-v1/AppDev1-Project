from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    pwd = db.Column(db.String(), nullable=False)
    followers_count = db.Column(db.Integer(), nullable=False)
    following_count = db.Column(db.Integer(), nullable=False)
    posts_count = db.Column(db.Integer(), nullable=False)
    followers = db.Column(db.String(), nullable=True)
    following = db.Column(db.String(), nullable=True)
    posts = db.relationship('Post', secondary='UserPosts',
                            backref='User', cascade='all,delete')


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer(), nullable=False,
                   primary_key=True, autoincrement=True)
    creator = db.Column(db.String(), nullable=False)
    contains_img = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(), nullable=True)
    caption = db.Column(db.String(), nullable=True)
    img_id = db.Column(db.String(), nullable=True, unique=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=datetime.now, nullable=False)


class UserPosts(db.Model):
    __tablename__ = 'UserPosts'
    userpostID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), db.ForeignKey('User.id'))
    postID = db.Column(db.Integer(), db.ForeignKey('Post.id'))
