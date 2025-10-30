from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.group import Group
from app.services.group_services import Groupservice

group_bp = Blueprint('group_bp', __name__)

@group_bp.route('/add', methods=['POST'])
def add_group():
    data = request.get_json()

    if not data or 'group' not in data:
        print("No JSON data received!")
        return jsonify({"status": "error", "message": "provide group name!"}), 400
    
    try:
        group = Groupservice.create_group(data)

        return jsonify({
            "message": "Group created successfully!",
            "id": group.id,
            "group": group.group
        }), 201
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
