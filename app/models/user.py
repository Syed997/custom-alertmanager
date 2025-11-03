from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<URL {self.name}>"