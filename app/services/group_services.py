from app.extensions import db
from app.models.group import Group


class Groupservice:

    @staticmethod
    def create_group(data):
        group_name = data.get('group')

        if Group.query.filter_by(group=group_name).first():
            raise ValueError("Group already exists")

        new_group = Group(group=group_name)

        db.session.add(new_group)
        db.session.commit()

        return new_group
    
    @staticmethod
    def isvalid(group_name):
        return Group.query.filter_by(group=group_name).first()
    

    @staticmethod
    def get_all_groups():
        groups = Group.query.all()
        result = []
        for group in groups:
            result.append({
                "id": group.id,
                "group": group.group
            })

        return result