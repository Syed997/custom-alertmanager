from app.models.user import User
from app.extensions import db, bcrypt


class Userservice():

    @staticmethod
    def create_user(data):

        hashed_pass = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(mail=data['mail'], password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user
    

    @staticmethod
    def get_all_users():

        users = User.query.all()
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "mail": user.mail,
                "password": user.password,
                "created_at": user.created_at
            })

        return result
    
    @staticmethod
    def is_userexist(mail):
        user = User.query.filter_by(mail=mail).first()

        return user