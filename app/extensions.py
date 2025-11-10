from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis
from flask import current_app
from redis import StrictRedis


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

redis_client = None

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