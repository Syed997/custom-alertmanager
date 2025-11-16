from flask import Blueprint, request, jsonify
from app.utils.data_process import process_alert_data
from app.services.alert_generate import send_teams_alert, send_email_alert, send_sms_alert
import json
from app.services.group_services import Groupservice
from app.services.member_services import Memberservices

alert_bp = Blueprint('alert_bp', __name__)

@alert_bp.route('/teams', methods=['POST'])
def alert_teams():
    # raw_data = request.get_data(as_text=True)
    # print("Raw incoming data from SigNoz:")
    # print(raw_data)
    # print("-" * 50)

    data = request.get_json()
    if data:
        print("Parsed JSON data from SigNoz:")
        print(json.dumps(data, indent=2))
        print("-" * 50)
        
        alert_message = process_alert_data(data)
        
    else:
        print("No JSON data received – check Content-Type header.")
        alert_message = 'No data provided'

    success = send_teams_alert(alert_message)

    if success:
        return jsonify({"status": "success", "message": "Alert sent to Teams"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send alert"}), 500
    

@alert_bp.route('/<string:group>', methods=['POST'])
def alert(group):
    group_id = Groupservice.isvalid(group).id

    if not group_id:
        return jsonify({"error": "group does not exist."}), 400
    
    mails = Memberservices.get_mail(group_id)
    numbers = Memberservices.get_number(group_id)

    data = request.get_json()
    if data:
        print("Parsed JSON data from SigNoz:")
        print(json.dumps(data, indent=2))
        print("-" * 50)
        
        # Process the data and generate the alert message
        alert_message = process_alert_data(data)
        
    else:
        print("No JSON data received – check Content-Type header.")
        alert_message = 'No data provided'

        email_success = send_email_alert(alert_message, mails)
        sms_success = send_sms_alert(numbers, alert_message)

        if email_success and sms_success:
            return jsonify({"status": "success", "message": "Alert sent via Email and SMS"}), 200
        elif email_success:
            return jsonify({"status": "partial", "message": "Email sent but SMS failed"}), 207
        elif sms_success:
            return jsonify({"status": "partial", "message": "SMS sent but Email failed"}), 207
        else:
            return jsonify({"status": "error", "message": "Failed to send Email and SMS"}), 500 
    # success = send_email_alert(alert_message, mails)

    # if success:
    #     return jsonify({"status": "success", "message": "Alert sent to Mails"}), 200
    # else:
    #     return jsonify({"status": "error", "message": "Failed to send alert"}), 500
