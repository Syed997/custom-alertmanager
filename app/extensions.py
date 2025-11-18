from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis
from flask import current_app, jsonify
from redis import StrictRedis
from flask_migrate import Migrate


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
redis_client = None

def init_jwt(app):
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({
            "msg": "Missing Authorization Header",
            "error": reason
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({
            "msg": "Invalid token",
            "error": reason
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "msg": "Token has expired"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "msg": "Token has been revoked"
        }), 401


def init_redis(app):
    global redis_client
    redis_client = redis.StrictRedis(
        host=app.config.get("REDIS_HOST", "localhost"),
        port=app.config.get("REDIS_PORT", 6379),
        db=0,
        decode_responses=True
    )

def get_redis():
    global redis_client
    if redis_client is None:
        app = current_app
        redis_client = StrictRedis(
            host=app.config.get("REDIS_HOST", "localhost"),
            port=app.config.get("REDIS_PORT", 6379),
            db=app.config.get("REDIS_DB", 0),
            decode_responses=True
        )
    return redis_client