import requests, os, smtplib, json
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
    
def send_sms_alert(receivers, message):
    """
    Send SMS alert using Robi SMS API.
    """

    userName        = os.getenv("ROBI_SMS_USERNAME")
    password_digest = os.getenv("ROBI_SMS_PASSWORD_DIGEST")
    nonce           = os.getenv("ROBI_SMS_NONCE")
    created         = os.getenv("ROBI_SMS_CREATED")
    service_id      = os.getenv("ROBI_SMS_SERVICE_ID")
    api_url         = os.getenv("ROBI_SMS_API_URL")

    if not all([userName, password_digest, nonce, created, service_id, api_url]):
        print("❌ Missing SMS environment variables.")
        return False

    url = f"{api_url}/{userName}/requests"

    # ---- MOST IMPORTANT: EXACT ROBI WSSE HEADER FORMAT ----
    wsse_header = (
        f"UsernameToken Username={userName},"
        f"PasswordDigest={password_digest},"
        f"Nonce={nonce},"
        f"Created={created}"
    )

    request_header = (
        f'request ServiceId={service_id}, LinkId="", FA="", OA="", PresentId=""'
    )

    headers = {
        "X-WSSE": wsse_header,
        "X-RequestHeader": request_header,
        "Authorization": 'WSSE realm="SDP",profile="UsernameToken"',
        "Accept-Encoding": "gzip,deflate",
        "Accept": "application/json",
        "User-Agent": "Jakarta Commons-HttpClient/3.1",
        "Content-Type": "application/json; charset=UTF-8",
    }

    success = True

    for receiver in receivers:
        payload = {
            "outboundSMSMessageRequest": {
                "address": [str(receiver)],
                "senderAddress": "ApmAlrt",
                "outboundSMSTextMessage": {"message": message},
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code in (200, 201):
                print(f"📨 SMS sent successfully to {receiver}")
            else:
                print(f"❌ Failed to send SMS to {receiver} ({response.status_code})")
                print(response.text)
                success = False

        except Exception as e:
            print(f"❌ Exception sending SMS to {receiver}: {e}")
            success = False

    return success
