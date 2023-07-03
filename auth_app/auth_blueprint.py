from flask import Blueprint, render_template
from .models.user import User, db
from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user
from datetime import timedelta

duration = timedelta(hours=1)

auth_blueprint = Blueprint('auth_blueprint', __name__,  template_folder='templates')



# Initialize the db instance within the Blueprint
# db.init_app(auth_blueprint)
@auth_blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    data = {"valid": current_user.is_authenticated, "user": current_user}
    return render_template('login.html', data=data)





@auth_blueprint.route('/login', methods=['GET'])
def login_get():
    
    data = {"valid": current_user.is_authenticated, "user": current_user}
    return render_template('login.html', data=data)




@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    print("inside login post")
    # Check if 'data' field is present in the request body
    if 'data' not in data:
        return jsonify({"errors":[{'message': 'Invalid request body'}], "data": []}), 400

    # Extract the 'data' field
    user_data = data['data']

    # Check if the required fields are present in the user_data
    required_fields = ['email', 'password']
    missing_fields = [field for field in required_fields if field not in user_data]
    if missing_fields:
        errors = [{'field': field, 'message': f'Missing {field} field'} for field in missing_fields]
        return jsonify({'errors': errors, "data": data}), 400

    # Extract the values from user_data
    email = user_data['email']
    password = user_data['password']

    # Retrieve the user from the database based on the provided email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        # Use Flask-Login to log in the user and start a session
        login_user(user,  remember=True, duration=duration)
        print("created ")
        data["message"] = 'Logged in successfully'
        # Return a success response
        return jsonify({"data": data, "errors": []})

    # Return an error response if login credentials are invalid
    return jsonify({'errors': [{"message":'Invalid email or password'}], "data": {}}), 401





@auth_blueprint.route('/signup', methods=['GET'])
def signup_get():
    data = {"valid": current_user.is_authenticated, "user": current_user}
    return render_template('signup.html', data=data)


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    try:
        data = request.get_json()

        if 'data' not in data:
            return jsonify({'error': [{"message":'Invalid request body'}], "data": {}}), 400
        
        # Extract the 'data' field
        user_data = data['data']



        # Check if the required fields are present in the user_data
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            errors = [{'field': field, 'message': f'Missing {field} field'} for field in missing_fields]
            return jsonify({'errors': errors, "data":{}}), 400
        

        # Extract the values from user_data
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        # Check if a user with the given email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'errors': [{"message":'User with this email already exists'}], "data":{}}), 409
        

        # Create a new user instance
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        res = {"data": data, "errors": []}
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'errors': [{"message":'An error occurred during account creation','details': str(e)}]}), 500
