from flask import Blueprint, request, jsonify
from app.services.user_services import Userservice
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()

    if not data or not data['mail'] or not data['password']:
        return jsonify({"error": "give username and password"}), 400
    
    #TODO: check if the user exist
    
    new_user = Userservice.create_user(data)

    return jsonify({
        "message": "user created successfully",
        "id": new_user.id
    }), 201

@auth_bp.route('/get')
@jwt_required()
def user_lists():
    user_id = get_jwt_identity()
    users = Userservice.get_all_users()
    print(user_id)
    return jsonify(users), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Userservice.is_userexist(data['mail'])
    if not user:
        return jsonify({"unautorized": "user does not exist"}), 201
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"unautorized": "invalid password"}), 201
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access token": access_token
    }), 201
    


    
