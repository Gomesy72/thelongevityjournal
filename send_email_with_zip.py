#!/usr/bin/env python3
"""Send ZIP file via email"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

# Email config
USERNAME = "shellyai2026@gmail.com"
PASSWORD = "ygwkifjjdwhorvje"
RECIPIENT = "gomesy72@gmail.com"

def send_zip():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "The Longevity Journal - Deployment ZIP"
    msg["From"] = USERNAME
    msg["To"] = RECIPIENT
    
    body = """
    Hi Joe,
    
    Here's The Longevity Journal deployment package.
    
    To deploy:
    1. Unzip this file
    2. Go to github.com/gomesy72/thelongevityjournal
    3. Click "Add file" → "Upload files"
    4. Upload ALL unzipped files (index.html, styles.css, script.js, articles/ folder)
    5. Go to Settings → Pages → Enable GitHub Pages (main branch)
    6. Wait 2 minutes, visit: https://gomesy72.github.io/thelongevityjournal/
    
    Questions? Message Shelly!
    
    - The Longevity Journal Team
    """
    
    msg.attach(MIMEText(body, "plain"))
    
    # Attach ZIP
    zip_path = Path("C:\\Openclaw\\agents\\longevity-journal.zip")
    if zip_path.exists():
        with open(zip_path, 'rb') as f:
            part = MIMEBase('application', 'zip')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{zip_path.name}"')
            msg.attach(part)
        print(f"Attached: {zip_path.name}")
    else:
        print("ZIP file not found!")
        return
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)
    
    print(f"Email sent to {RECIPIENT}")

if __name__ == "__main__":
    send_zip()
