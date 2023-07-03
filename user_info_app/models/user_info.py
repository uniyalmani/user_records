from flask_sqlalchemy import SQLAlchemy

from extensions import db

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_info', cascade='all, delete-orphan'))
    
    def __init__(self, college, name, user):
        self.college = college
        self.name = name
        self.user = user
    

    