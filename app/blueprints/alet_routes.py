from flask import Blueprint, request, jsonify
from app.utils.data_process import process_alert_data
from app.services.teamsnotification import send_teams_alert
import json

alert_bp = Blueprint('alert_bp', __name__)

@alert_bp.route('/', methods=['POST'])
def alert():
    # raw_data = request.get_data(as_text=True)
    # print("Raw incoming data from SigNoz:")
    # print(raw_data)
    # print("-" * 50)

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

    success = send_teams_alert(alert_message)

    if success:
        return jsonify({"status": "success", "message": "Alert sent to Teams"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send alert"}), 500