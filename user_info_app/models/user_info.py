from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from extensions import db
from werkzeug.utils import secure_filename
from flask import current_app
import os

class UserFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    file_format = db.Column(db.String(10), nullable=False)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)

    def save_file(self, file, title, description):
        name =  current_user.email + file.filename
        secure_name = secure_filename(name)
        file_path = os.path.join(current_app.config['FILE_LOCATION'], secure_name)
        file.save(file_path)
        self.name = secure_name
        self.title = title
        self.file_format = os.path.splitext(secure_name)[1][1:]
        self.description = description
        

    def get_file_path(self):
        return os.path.join(current_app.config['FILE_LOCATION'], self.name)

    @staticmethod
    def get_all_files():
        return UserFiles.query.all()

    @staticmethod
    def search_files_by_user_email(user_email):
        return UserFiles.query.filter(UserFiles.user_email.ilike(f"%{user_email}%")).all()

    @staticmethod
    def search_files_by_title(title):
        return UserFiles.query.filter(UserFiles.title.ilike(f"%{title}%")).all()

    

    