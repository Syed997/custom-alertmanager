from flask import Blueprint, request, jsonify
from app.services.member_services import Memberservices

groupmember_bp = Blueprint('groupmember_bp', __name__)

@groupmember_bp.route('/add', methods=['POST'])
def addmember():
    data = request.get_json()
    print(data)
    #TODO: need to load the request data into marshmallow to validation check

    try:
        member = Memberservices.create_member(data)

        return jsonify({
            "success": "member created!",
            "id": member.id
        }), 201
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@groupmember_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    try:
        member = Memberservices.update_member(member_id, data)
        return jsonify({
            "id": member.id,
            "name": member.name,
            "mail": member.mail,
            "mobile": member.m_number,
            "group_id": member.group_id
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@groupmember_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = Memberservices.delete_member(member_id)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



@groupmember_bp.route('/')
def fetchmembers():
    members = Memberservices.get_all_members()
    return jsonify(members), 200
     