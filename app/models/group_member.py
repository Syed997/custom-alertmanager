from app.extensions import db

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(30), nullable=False, unique=False)
    m_number = db.Column(db.Integer, nullable=False, unique=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    group = db.relationship('Group', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<URL {self.name}>"