import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "shellyai2026@gmail.com"
SENDER_PASSWORD = "ygwkifjjdwhorvje"

def send_welcome_email(recipient_email, recipient_name=""):
    """Send a branded welcome email to new subscriber"""
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome to The Longevity Journal — Your Journey Starts Here!"
    msg['From'] = f"The Longevity Journal <{SENDER_EMAIL}>"
    msg['To'] = recipient_email
    
    # Personalized greeting
    greeting = f"Hey {recipient_name}," if recipient_name else "Hey there,"
    
    # HTML body
    html_body = f"""
    <div style="max-width:600px;margin:0 auto;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;color:#0e0e0e;">
      
      <div style="background:#0e0e0e;padding:40px 30px;text-align:center;">
        <div style="font-family:'Courier New',monospace;font-size:11px;text-transform:uppercase;letter-spacing:0.15em;color:#74c69d;margin-bottom:8px;">TLJ</div>
        <h1 style="font-family:Georgia,serif;font-size:28px;font-weight:900;color:#f5f0e8;margin:0;line-height:1.1;">The Longevity Journal</h1>
        <p style="font-size:11px;text-transform:uppercase;letter-spacing:0.2em;color:#8a8070;margin-top:6px;">AI-Curated Research · Human-Tested</p>
      </div>
      
      <div style="padding:40px 30px;background:#ffffff;">
        
        <p style="font-size:16px;line-height:1.7;color:#4a4a4a;margin-bottom:20px;">{greeting}</p>
        
        <p style="font-size:16px;line-height:1.7;color:#4a4a4a;margin-bottom:20px;">Welcome to The Longevity Journal! I'm thrilled you've joined our community of people who refuse to accept that aging is inevitable.</p>
        
        <p style="font-size:16px;line-height:1.7;color:#4a4a4a;margin-bottom:20px;">Every week, our AI agents scan 200+ scientific sources to bring you the most promising research — distilled into 5-minute reads you can actually understand.</p>
        
        <div style="background:#ecfdf5;border-left:4px solid #2d6a4f;padding:20px;margin:30px 0;">
          <h3 style="color:#065f46;margin:0 0 10px 0;font-size:18px;font-weight:700;">What You'll Get Every Week:</h3>
          <p style="color:#047857;margin:0;font-size:15px;line-height:1.6;">
            <strong>Monday:</strong> The latest breakthroughs in longevity science<br>
            <strong>Wednesday:</strong> Deep dives into supplements, diets, and protocols<br>
            <strong>Friday:</strong> Practical tips you can implement today
          </p>
        </div>
        
        <p style="font-size:16px;line-height:1.7;color:#4a4a4a;margin-bottom:20px;">All content is fact-checked, written for humans (not scientists), actionable, and free from sponsored content bias.</p>
        
        <h3 style="font-family:Georgia,serif;font-size:22px;font-weight:700;color:#0e0e0e;margin:40px 0 20px 0;">Start Reading:</h3>
        
        <div style="background:#f9fafb;border-radius:8px;padding:24px;margin:20px 0;border-left:4px solid #2d6a4f;">
          <h4 style="margin:0 0 10px 0;font-size:18px;font-weight:700;color:#0e0e0e;">NAD+ Precursors: The $2 Billion Anti-Aging Bet</h4>
          <p style="color:#6b7280;margin:0 0 12px 0;font-size:14px;line-height:1.5;">NR vs NMN vs Niacin — what the latest human trials actually show about these popular supplements.</p>
          <a href="https://gomesy72.github.io/thelongevityjournal/nad-precursors.html" style="color:#2d6a4f;text-decoration:none;font-weight:600;font-size:14px;">Read Now →</a>
        </div>
        
        <div style="background:#f9fafb;border-radius:8px;padding:24px;margin:20px 0;border-left:4px solid #2d6a4f;">
          <h4 style="margin:0 0 10px 0;font-size:18px;font-weight:700;color:#0e0e0e;">Why Zone 2 Cardio is the Cheat Code for Longevity</h4>
          <p style="color:#6b7280;margin:0 0 12px 0;font-size:14px;line-height:1.5;">Elite athletes and centenarians both swear by it. Here's the science behind low-intensity exercise.</p>
          <a href="https://gomesy72.github.io/thelongevityjournal/zone-2-cardio.html" style="color:#2d6a4f;text-decoration:none;font-weight:600;font-size:14px;">Read Now →</a>
        </div>
        
        <div style="text-align:center;margin:40px 0;">
          <a href="https://gomesy72.github.io/thelongevityjournal/" style="display:inline-block;background:#2d6a4f;color:#ffffff;padding:15px 30px;text-decoration:none;border-radius:4px;font-weight:600;font-size:16px;">Visit The Longevity Journal</a>
        </div>
        
        <p style="font-size:16px;line-height:1.7;color:#4a4a4a;margin-bottom:10px;">Here's to living longer and better,</p>
        <p style="font-size:16px;font-weight:700;color:#0e0e0e;margin:0;">The Longevity Journal Team</p>
        
      </div>
      
      <div style="background:#f9fafb;padding:30px;text-align:center;border-top:1px solid #e5e7eb;">
        <p style="font-size:13px;color:#8a8070;margin:0 0 5px 0;">You're receiving this because you subscribed to The Longevity Journal.</p>
        <p style="font-size:13px;color:#8a8070;margin:0 0 5px 0;"><a href="https://gomesy72.github.io/thelongevityjournal/privacy-policy.html" style="color:#2d6a4f;text-decoration:none;">Privacy Policy</a> | <a href="https://gomesy72.github.io/thelongevityjournal/terms-of-service.html" style="color:#2d6a4f;text-decoration:none;">Terms</a></p>
        <p style="font-size:13px;color:#8a8070;margin:0;">The Longevity Journal | AI-Curated Research, Human-Tested</p>
      </div>
      
    </div>
    """
    
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"SUCCESS: Welcome email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"FAILED: Could not send email to {recipient_email}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_manual_welcome.py <email> [name]")
        print("Example: python send_manual_welcome.py joe@example.com Joe")
        sys.exit(1)
    
    email = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else ""
    
    success = send_welcome_email(email, name)
    sys.exit(0 if success else 1)
