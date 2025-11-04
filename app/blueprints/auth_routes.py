from flask import Blueprint, request, jsonify
from app.services.user_services import Userservice

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
def user_lists():
    users = Userservice.get_all_users()

    return jsonify(users), 200



    
