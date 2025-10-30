from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.group import Group

group_bp = Blueprint('group_bp', __name__)

@group_bp.route('/add', methods=['POST'])
def add_group():
    data = request.get_json()

    if not data or 'group' not in data:
        print("No JSON data received!")
        return jsonify({"status": "error", "message": "provide group name!"}), 400
    
    group_name = data.get('group')
    new_group = Group(group=group_name)
    try:
        db.session.add(new_group)
        db.session.commit()
        return jsonify({
            "message": "Group created successfully!",
            "id": new_group.id,
            "group": new_group.group
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
