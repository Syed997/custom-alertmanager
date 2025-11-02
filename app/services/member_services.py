from app.extensions import db
from app.models.group_member import Member
from app.services.group_services import Groupservice

class Memberservices:

    @staticmethod
    def create_member(data):

        group = Groupservice.isvalid(data['group'])
        if not group:
            raise ValueError('Group does not exist')
        
        member = Member(
            name = data['name'],
            mail = data['mail'],
            m_number = data['mobile'],
            group_id = group.id
        )

        db.session.add(member)
        db.session.commit()

        return member
    
    @staticmethod
    def get_all_members():
        members = Member.query.all()
        result = []
        for member in members:
            result.append({
                "id": member.id,
                "name": member.name,
                "mail": member.mail,
                "mobile": member.m_number,
                "group": member.group.group
            })

        return result
    
    @staticmethod
    def update_member(member_id, data):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found")

        # Update only if key exists in data
        if 'name' in data:
            member.name = data['name']
        if 'mail' in data:
            member.mail = data['mail']
        if 'mobile' in data:
            member.m_number = data['mobile']
        if 'group' in data:
            group = Groupservice.isvalid(data['group'])
            if not group:
                raise ValueError("Group does not exist")
            member.group_id = group.id

        db.session.commit()
        return member
    
    @staticmethod
    def delete_member(member_id):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found")

        db.session.delete(member)
        db.session.commit()
        return {"message": f"Member with ID {member_id} deleted successfully"}


    @staticmethod
    def get_mail(group_id):
        mails = [member.mail for member in Member.query.filter_by(group_id=group_id).all()]
        return mails
    
    @staticmethod
    def get_number(group_id):
        numbers = [member.m_number for member in Member.query.filter_by(group_id=group_id).all()]
        return numbers