import os
import sys
import json
import smtplib
import subprocess
from datetime import datetime
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration
BASE_DIR = Path(__file__).parent
WEBSITE_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Email config
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "shellyai2026@gmail.com",
    "sender_password": "ygwkifjjdwhorvje",
}

# ConvertKit config
CONVERTKIT_CONFIG = {
    "form_id": "9441355",
    "user_id": "0647d69e35",
}

# Topics to rotate through
TOPICS = [
    "rapamycin",
    "nad-boosters",
    "fasting-protocols",
    "senolytics",
    "metformin",
    "omega-3",
    "sleep-optimization",
    "zone-2-cardio",
    "spermidine",
    "epigenetic-reprogramming"
]

def generate_article(topic):
    """Generate article using Ollama"""
    prompt = f"""Write a comprehensive 2000-word article about {topic} for longevity.
    
    Structure:
    1. Introduction - why this matters for longevity
    2. The Science - mechanisms and research
    3. Human Evidence - clinical trials and studies
    4. Practical Application - dosage, timing, sources
    5. Risks and Considerations - side effects, contraindications
    6. Key Takeaways - actionable summary
    
    Style: Evidence-based, cautious claims, actionable takeaways.
    Reading level: 10th grade.
    Include inline citations where possible.
    """
    
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma4:31b", prompt],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout
    except Exception as e:
        print(f"Error generating article: {e}")
        return None

def convert_to_html(markdown_content, title):
    """Convert markdown to HTML"""
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="article-page">
        <div class="article-meta-bar">
            <span class="category">Research</span>
            <span class="date">{datetime.now().strftime('%B %d, %Y')}</span>
            <span class="read-time">8 min read</span>
        </div>
        <div class="article-content">
            {markdown_content}
        </div>
    </div>
</body>
</html>
"""
    return html_template

def send_newsletter(subject, html_content, recipient_list):
    """Send newsletter to subscribers"""
    for recipient in recipient_list:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"The Longevity Journal <{EMAIL_CONFIG['sender_email']}>"
            msg['To'] = recipient
            
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                server.send_message(msg)
            
            print(f"Newsletter sent to {recipient}")
        except Exception as e:
            print(f"Failed to send to {recipient}: {e}")

def run_pipeline():
    """Run the full weekly pipeline"""
    print("=" * 60)
    print("THE LONGEVITY JOURNAL - WEEKLY PIPELINE")
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Generate article
    topic = TOPICS[datetime.now().isocalendar()[1] % len(TOPICS)]
    print(f"\n1. Generating article on: {topic}")
    
    article_content = generate_article(topic)
    if not article_content:
        print("FAILED: Article generation failed")
        return False
    
    # 2. Convert to HTML
    print("\n2. Converting to HTML...")
    title = f"The Science of {topic.replace('-', ' ').title()}"
    html_content = convert_to_html(article_content, title)
    
    # 3. Save article
    article_filename = f"{topic}-{datetime.now().strftime('%Y%m%d')}.html"
    article_path = WEBSITE_DIR / article_filename
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Article saved: {article_path}")
    
    # 4. Update index.html to include new article
    print("\n3. Updating website index...")
    # This would update the index.html to link to the new article
    
    # 5. Deploy to GitHub
    print("\n4. Deploying to GitHub...")
    try:
        subprocess.run(
            ["git", "add", "."],
            cwd=WEBSITE_DIR,
            check=True
        )
        subprocess.run(
            ["git", "commit", "-m", f"Weekly article: {title}"],
            cwd=WEBSITE_DIR,
            check=True
        )
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=WEBSITE_DIR,
            check=True
        )
        print("Deployed successfully!")
    except Exception as e:
        print(f"Deploy failed: {e}")
    
    # 6. Send newsletter
    print("\n5. Sending newsletter...")
    # Get subscribers from ConvertKit or local list
    subscribers = ["gomesy61@gmail.com"]  # Add more as they subscribe
    
    newsletter_subject = f"Weekly Brief: {title}"
    send_newsletter(newsletter_subject, html_content, subscribers)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running in TEST mode...")
        # Test with a shorter article
        test_topic = "sleep-optimization"
        article = generate_article(test_topic)
        if article:
            print("\nTest article generated successfully!")
            print(f"Length: {len(article)} characters")
        else:
            print("Test failed!")
    else:
        run_pipeline()
