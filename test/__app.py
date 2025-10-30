from flask import Flask, request, jsonify
import requests
import json  # For pretty-printing if needed

app = Flask(__name__)

# Replace this with your actual Teams webhook URL
TEAMS_WEBHOOK_URL = "http://10.104.10.140:7072/webhookb2/8b4ab1d6-8e0e-48c6-9b4f-c7dbaa2247de@255b709d-ce46-478e-b485-e237f988c923/IncomingWebhook/c34d686f730041b5ad3612167be2e23e/dcdbeb11-e5de-43ca-b8c4-a14b41f3e3f4/V209r4SuVb34qascf3f7Ig7zsm4z18rbSPUhoorn9OD8A1"

def send_teams_alert(message):
    """Send alert to Microsoft Teams via webhook"""
    payload = {
        "text": f"🚨 Alert from Flask API Signoz:\n\n{message}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(TEAMS_WEBHOOK_URL, json=payload, headers=headers)
    return response.status_code == 200


@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    """API endpoint to trigger an alert"""
    # Print the raw incoming data from SigNoz for debugging
    raw_data = request.get_data(as_text=True)
    print("Raw incoming data from SigNoz:")
    print(raw_data)
    print("-" * 50)
    
    # Parse JSON and print it (pretty-printed for readability)
    data = request.get_json()
    if data:
        print("Parsed JSON data from SigNoz:")
        print(json.dumps(data, indent=2))
        print("-" * 50)
        
        # Now process as before (you may need to adjust based on actual SigNoz payload structure)
        # SigNoz/AlertManager typically sends a dict with 'alerts' (list), 'groupLabels', etc.
        # For now, falling back to 'message' – check the print output and update this logic if needed
        alert_message = data.get('message', 'No message provided')
        
        # If it's AlertManager format, extract a better message, e.g.:
        # if 'alerts' in data and data['alerts']:
        #     alert = data['alerts'][0]
        #     alert_message = f"Alert: {alert.get('annotations', {}).get('summary', 'Unknown')}\nDetails: {alert.get('annotations', {}).get('description', '')}"
        
    else:
        print("No JSON data received – check Content-Type header.")
        data = {}  # Fallback
        alert_message = 'No data provided'

    success = send_teams_alert(alert_message)
    if success:
        return jsonify({"status": "success", "message": "Alert sent to Teams"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send alert"}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)