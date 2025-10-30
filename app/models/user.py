from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(30), nullable=False)
    m_number = db.Column(db.Integer(11), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    group = db.relationship('Group', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<URL {self.name}>"