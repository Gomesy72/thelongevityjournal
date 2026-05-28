import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Load config
config_path = Path(__file__).parent / "email_config.json"
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
else:
    # Default config
    config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "shellyai2026@gmail.com",
        "sender_password": "ygwkifjjdwhorvje",  # App password
    }

# The email to send to
recipient_email = "gomesy61@gmail.com"  # Joe's subscribed email

# Read the HTML email content
html_path = Path(__file__).parent / "welcome_email.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = "Welcome to The Longevity Journal - Your Journey Starts Here!"
msg['From'] = f"The Longevity Journal <{config['sender_email']}>"
msg['To'] = recipient_email

# Attach HTML content
msg.attach(MIMEText(html_content, 'html'))

# Send email
try:
    with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
        server.starttls()
        server.login(config['sender_email'], config['sender_password'])
        server.send_message(msg)
    print(f"SUCCESS: Welcome email sent to {recipient_email}")
except Exception as e:
    print(f"FAILED to send email: {e}")
