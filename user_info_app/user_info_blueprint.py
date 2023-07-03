from flask import request, jsonify, redirect, render_template
from flask_login import login_required, current_user
from .models.user_info import UserInfo, db
from flask import Blueprint, jsonify, request



user_info_blueprint = Blueprint('user_info_blueprint', __name__, template_folder='templates')



@user_info_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})
    
    
    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return  render_template('profile.html', data=data)





@user_info_blueprint.route('/list_added_user', methods=['GET'])
@login_required
def list_added_user():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})
    
    user_info_list = UserInfo.query.filter_by(user=current_user).all()
    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return  render_template('user_info_list.html', user_info = user_info_list, data=data)



@user_info_blueprint.route('/add_user', methods=['GET'])
@login_required
def add_user_get():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})

    data =  {"valid": current_user.is_authenticated, "user": current_user}
    return render_template('add_user_info.html', data=data)


@user_info_blueprint.route('/add_user', methods=['POST'])
@login_required
def add_user_post():
    if not current_user.is_authenticated:
        return redirect('/login', flash={'error': "session expire please login"})

    data = request.get_json()

    required_fields = ['college', 'name']
    missing_fields = [field for field in required_fields if field not in data['data']]
    if missing_fields:
        return jsonify({'errors': [{f'Missing required fields: {", ".join(missing_fields)}'}], "data":{} }), 400

    college = data['data'].get('college')
    name = data['data'].get('name')

    # Create UserInfo object and associate it with the current user
    user_info = UserInfo(college=college, name=name, user=current_user)

    try:
        # Add and commit the UserInfo object to the database
        db.session.add(user_info)
        db.session.commit()
        print(data)
        return jsonify({"data": data, "errors": []}), 200
    except Exception as e:
        return jsonify({'errors':[{"message" :str(e)}], "data": {}}), 500


