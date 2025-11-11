import random
from flask import Blueprint, request, jsonify
from app.schemas.user_schemas import UserSignUpSchema
from app.services.user_services import Userservice
from app.extensions import bcrypt, redis_client, get_redis
from app.services.alert_generate import mail_verify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    schema = UserSignUpSchema()

    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


    if not data or not data['mail'] or not data['password']:
        return jsonify({"error": "give username and password"}), 401
    
    user = Userservice.is_userexist(data['mail'])
    if user:
        return jsonify({"error": "user exist"}), 401
    
    verification_code = str(random.randint(100000, 999999))
    redis_client = get_redis()
    redis_client.setex(f"verify_{data['mail']}", 300, verification_code)

    success = mail_verify(data['mail'], verification_code)

    if not success:
        return jsonify({"error": "failed to send verification mail"}), 500
    return jsonify({
        "message": "verification code sent to mail"
    }), 200



@auth_bp.route('/signup/verify', methods=['POST'])
def sign_up_verify():
    data = request.get_json()

    if not data or not data['mail'] or not data['password']:
        return jsonify({"error": "give username and password"}), 401
    
    #TODO: check if the user exist

    if 'otp' not in data:
        return jsonify({"error": "provide verification code"}), 400
    
    redis_client = get_redis()
    stored_code = redis_client.get(f"verify_{data['mail']}")

    if not stored_code or stored_code != data['otp']:
        return jsonify({"error": "invalid or expired verification code"}), 400
    
    #TODO: need to load the request data into marshmallow to validation check
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
        return jsonify({"unautorized": "user does not exist"}), 401
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"unautorized": "invalid password"}), 401
    
    access_token = create_access_token(identity=str(user.id))

    #TODO: set the token in redis with expiry
    #TODO: need to implement logout to delete the token from redis
    #TODO: need to implement token refresh

    return jsonify({
        "access token": access_token
    }), 201


@auth_bp.route('/redis')
def test_redis():
    try:
        redis_client = get_redis()
        redis_client.setex('test_key', 10, 'Hello, Redis with TTL!')
        value = redis_client.get('test_key')
        ttl = redis_client.ttl('test_key')
        return jsonify({
            "redis_value": value,
            "expires_in_seconds": ttl
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
