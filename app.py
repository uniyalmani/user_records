from flask import Flask, render_template, request,send_from_directory
from config import AppSettings
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from auth_app.auth_blueprint import auth_blueprint
from user_info_app.user_info_blueprint import user_info_blueprint
from auth_app.models.user import User
from extensions import db


app = Flask(__name__)
settings = AppSettings()

app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
app.config['SECRET_KEY'] = settings.secret_key
app.config['FILE_LOCATION'] = settings.file_location


db.init_app(app)
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)




app.register_blueprint(auth_blueprint)
app.register_blueprint(user_info_blueprint)

# Create all database tables
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.route('/files/<path:filename>')
def get_file(filename):
    directory =  app.config['FILE_LOCATION'] # Update with your directory path
    return send_from_directory(directory, filename)

@app.route('/')
def home():
    data =  {"valid" :current_user.is_authenticated, "user": current_user
             }
    return render_template('home.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)