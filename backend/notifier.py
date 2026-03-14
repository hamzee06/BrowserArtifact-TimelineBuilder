import json
from datetime import datetime
from plyer import notification
import smtplib
from email.mime.text import MIMEText

LOG_FILE = "realtime_logs/alerts_log.json"

def log_alert(message):
    """Save alert message to a JSON log file."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alert": message
    }
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def show_popup(message):
    """Show desktop notification."""
    notification.notify(
        title="Browser Monitor Alert",
        message=message,
        timeout=10
    )

def send_email_alert(subject, message, to_email="youremail@example.com"):
    """Send email alert using SMTP."""
    sender = "youralertemail@example.com"
    password = "your_email_password"  # Use App Password if Gmail
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
    except Exception as e:
        print(f"[ERROR] Email sending failed: {e}")
