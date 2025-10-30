from flask import Flask
from app.blueprints.alet_routes import alert_bp
from app.extensions import db
from config import DevConfig

def create_app(config_class=DevConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)

    app.register_blueprint(alert_bp, url_prefix='/alert')

    return app