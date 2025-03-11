from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Slogan(db.Model):
    __tablename__ = 'slogans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slogan = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'<Slogan {self.slogan}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'slogan': self.slogan
        }
