from flask import Flask
from app.blueprints.alet_routes import alert_bp
from app.blueprints.group_routes import group_bp
from app.blueprints.groupmember_routes import groupmember_bp
from app.blueprints.auth_routes import auth_bp
from flask_cors import CORS
from app.extensions import db, bcrypt, jwt, init_redis, init_jwt
from config import DevConfig

def create_app(config_class=DevConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    # jwt.init_app(app)
    init_jwt(app)
    # init_redis(app)
    

    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    CORS(app)
    app.register_blueprint(alert_bp, url_prefix='/alert')
    app.register_blueprint(group_bp, url_prefix='/groups')
    app.register_blueprint(groupmember_bp, url_prefix='/members')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app