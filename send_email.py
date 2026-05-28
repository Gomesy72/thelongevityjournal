#!/usr/bin/env python3
"""Send Longevity Journal HTML file via email"""

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

def send_html_file():
    """Send the HTML file as email attachment"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"The Longevity Journal - Sample Website ({datetime.now().strftime('%Y-%m-%d')})"
    msg["From"] = USERNAME
    msg["To"] = RECIPIENT
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; padding: 20px;">
    <h1 style="color: #0ff;">The Longevity Journal</h1>
    <p>Your sample website is attached!</p>
    <p><strong>Files included:</strong></p>
    <ul>
        <li>index.html - Main landing page</li>
        <li>styles.css - Dark theme styling</li>
        <li>script.js - Newsletter form handler</li>
        <li>articles/nad-precursors.html - Sample article</li>
    </ul>
    <p><strong>To view:</strong> Download and open index.html in your browser.</p>
    <p style="color: #888; margin-top: 20px;">Built by AI Agents | OpenClaw</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, "html"))
    
    # Attach files
    base_dir = Path(__file__).parent
    files_to_attach = [
        base_dir / "index.html",
        base_dir / "styles.css",
        base_dir / "script.js",
        base_dir / "articles" / "nad-precursors.html"
    ]
    
    for file_path in files_to_attach:
        if file_path.exists():
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{file_path.name}"'
                )
                msg.attach(part)
            print(f"Attached: {file_path.name}")
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)
    
    print(f"Email sent to {RECIPIENT}")

if __name__ == "__main__":
    send_html_file()
