from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    isUser = db.Column(db.Boolean, default=True)
    isCreator = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)

    # For one to many relatiship --> User(One) ---> Song(Many)
    songs = db.relationship('Song', backref='user', lazy=True)



class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    lyrics = db.Column(db.String, default='')
    duration = db.Column(db.String, default='')
    date = db.Column(db.String, default='')
    rating = db.Column(db.String, default='')

    isBlacklisted = db.Column(db.Boolean, default=False)

    # For one to many relatiship --> User(One) ---> Song(Many)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)