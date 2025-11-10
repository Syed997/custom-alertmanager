import requests, os, smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def send_teams_alert(message):
    """Send alert to Microsoft Teams via webhook"""
    payload = {
        "text": f"Alert from Flask API SigNoz:\n\n{message}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(TEAMS_WEBHOOK_URL, json=payload, headers=headers)
    return response.status_code == 200


def send_email_alert(message, recipients):
    """Send alert via email using SMTP"""
    try:
        subject = "Alert from Flask API SigNoz"
        body = f"{message}"

        # Create the email
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(recipients)  # visible To header

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            # Uncomment if authentication required
            # server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())

        print(f"Email sent successfully to: {', '.join(recipients)}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def mail_verify(recipient, code):
    """Send alert via email using SMTP"""
    try:
        subject = "Verification Code from Flask API SigNoz"
        body = f"Your verification code is {code}"

        # Create the email
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient  # visible To header

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            # Uncomment if authentication required
            # server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())

        print(f"Email sent successfully to: {recipient}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
