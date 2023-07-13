from flask import request, jsonify, redirect, render_template, url_for
from flask_login import login_required, current_user
from .models.user_info import  db, UserFiles
from flask import Blueprint, jsonify, request, current_app


user_info_blueprint = Blueprint('user_info_blueprint', __name__, template_folder='templates')



@user_info_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})
    
    
    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return  render_template('profile.html', data=data)





@user_info_blueprint.route('/list_all_files', methods=['GET'])
def list_added_files():
    
    query = request.args.get('filter', "all")
    print(query, "lllllllllll")
    if query == "all":
        user_files = UserFiles.get_all_files()
    else:
        email = request.args.get('email')
        title = request.args.get('title')
        if email:
            user_files = UserFiles.search_files_by_user_email(email)
        if title:
            user_files = UserFiles.search_files_by_title(title)

    base_url = current_app.config['FILE_LOCATION']
        
        
    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return  render_template('user_info_list.html', user_info = user_files, data=data, base_url = base_url)



@user_info_blueprint.route('/add_file', methods=['GET'])
@login_required
def add_user_get():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})

    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return render_template('add_files.html', data=data)


@user_info_blueprint.route('/add_file', methods=['POST'])
@login_required
def add_user_post():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})
    
    

    file = request.files['file']
    
    title = request.form['title']
    description = request.form['description']
    user = current_user
    user_file = UserFiles(user_email=current_user.email)
    user_file.save_file(file, title, description)
    db.session.add(user_file)
    db.session.commit()
    
    return redirect(url_for('user_info_blueprint.list_added_files'))

