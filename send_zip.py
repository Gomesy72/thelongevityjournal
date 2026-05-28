#!/usr/bin/env python3
"""Send Longevity Journal ZIP file via email"""

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
RECIPIENT = "shellyai2026@gmail.com"

def send_zip():
    """Send the ZIP file as email attachment"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"The Longevity Journal - Website Files ({datetime.now().strftime('%Y-%m-%d')})"
    msg["From"] = USERNAME
    msg["To"] = RECIPIENT
    
    body = """
    <html>
    <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; padding: 20px;">
    <h1 style="color: #0ff;">The Longevity Journal</h1>
    <p>Your website files are attached as a ZIP archive.</p>
    <p><strong>To view:</strong></p>
    <ol>
        <li>Download the ZIP file</li>
        <li>Extract all files</li>
        <li>Open <strong>index.html</strong> in your browser</li>
    </ol>
    <p><strong>Files included:</strong></p>
    <ul>
        <li>index.html - Main landing page</li>
        <li>styles.css - Dark theme styling</li>
        <li>script.js - Newsletter form handler</li>
        <li>articles/nad-precursors.html - Sample article</li>
    </ul>
    <p style="color: #888; margin-top: 20px;">Built by AI Agents | OpenClaw</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, "html"))
    
    # Attach ZIP file
    zip_path = Path(__file__).parent / "longevity-journal.zip"
    if zip_path.exists():
        with open(zip_path, 'rb') as f:
            part = MIMEBase('application', 'zip')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{zip_path.name}"'
            )
            msg.attach(part)
        print(f"Attached: {zip_path.name}")
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)
    
    print(f"Email sent to {RECIPIENT}")

if __name__ == "__main__":
    send_zip()
