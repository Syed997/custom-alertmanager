from flask import Flask
from app.blueprints.alet_routes import alert_bp
from app.blueprints.group_routes import group_bp
from app.blueprints.groupmember_routes import groupmember_bp
from app.extensions import db
from config import DevConfig

def create_app(config_class=DevConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)

    app.register_blueprint(alert_bp, url_prefix='/alert')
    app.register_blueprint(group_bp, url_prefix='/group')
    app.register_blueprint(groupmember_bp, url_prefix='/groupmember')
    return app