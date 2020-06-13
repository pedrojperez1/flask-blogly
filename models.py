"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )
    
    last_name = db.Column(
        db.String(30),
        nullable=False,
    )
    
    image_url = db.Column(
        db.String,
        nullable=True,
        server_default='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/User_font_awesome.svg/512px-User_font_awesome.svg.png'
    )

    def get_full_name(self):
        """Returns the user's full name"""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        """Better repr dunder for User"""
        return f'<User {self.first_name} {self.last_name} id={self.id}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    content = db.Column(
        db.String,
        nullable=False,
    )

    created_time = db.Column(
        db.DateTime,
        server_default=func.now(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
    )

    user = db.relationship('User', backref='posts')
