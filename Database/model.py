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
    posts = db.relationship('Post', secondary='user_posts',
                            lazy=True, backref=db.backref("User", lazy=True))


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=True)
    caption = db.Column(db.String(), nullable=True)
    # Image = db.Column(db.String(), nullable=True)
    img_id = db.Column(db.String(), nullable=True, unique=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                          default=datetime.now, nullable=False)


# class UserPost(db.Model):
#     __tablename__ = 'user_post'
#     userpostID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     userID = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     postID = db.Column(db.Integer(), db.ForeignKey('post.id'))

user_posts = db.Table('user_posts',
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          User.id), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey(
                          Post.id), primary_key=True)
                      )
