
from app import db
from datetime import date


class User(db.Model):
    __bind_key__ = 'user'
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(20), unique=True)


    def __init__(self, first_name, username, email, password):
        self.first_name = first_name
        self.username = username
        self.email = email
        self.password = password


class Articles(db.Model):
    __tablename__= 'articles'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(50), unique=True)
    content = db.Column('body', db.String(255))
    created_date = db.Column(db.DateTime)
    author = db.Column(db.String(80))


    def __init__(self, title, content, author, created_date=None):
        self.title = title
        self.content = content
        if created_date == None:
            created_date = date.today()
        self.created_date = created_date
        self.author = author