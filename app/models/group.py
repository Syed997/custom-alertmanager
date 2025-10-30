from app.extensions import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<URL {self.name}>"