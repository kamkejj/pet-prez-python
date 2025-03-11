from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    pet_name = db.Column(db.String(50), nullable=True)
    pet_species = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'pet_name': self.pet_name,
            'pet_species': self.pet_species,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Slogan(db.Model):
    __tablename__ = 'slogans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    slogan = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationship
    user = db.relationship('User', backref=db.backref('slogans', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'slogan': self.slogan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
