import markdown
import html
import sys
from datetime import datetime
from pathlib import Path

# Fix Unicode encoding for Windows
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# Fallback for older Python versions
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
BASE_DIR = Path(__file__).parent
WEBSITE_DIR = BASE_DIR

# Articles to convert
ARTICLES = [
    {
        "file": "senolytics_article.md",
        "topic": "senolytics",
        "title": "The Science of Senolytics: Can Clearing 'Zombie Cells' Extend Healthy Lifespan?",
        "category": "Research",
        "read_time": "10 min read",
        "date": "May 28, 2026"
    },
    {
        "file": "rapamycin_article.md",
        "topic": "rapamycin",
        "title": "Rapamycin: The Anti-Aging Drug From Easter Island",
        "category": "Supplements",
        "read_time": "12 min read",
        "date": "May 29, 2026"
    },
    {
        "file": "nad_boosters_article.md",
        "topic": "nad-boosters",
        "title": "NAD+ Boosters: NMN vs NR vs Niacin — The $500M Question",
        "category": "Supplements",
        "read_time": "11 min read",
        "date": "May 29, 2026"
    },
    {
        "file": "zone2_article.md",
        "topic": "zone2-cardio",
        "title": "Zone 2 Cardio: The Exercise Prescription for Longevity",
        "category": "Exercise",
        "read_time": "9 min read",
        "date": "May 29, 2026"
    }
]

def create_article_html(content, title, topic, category, read_time, date):
    """Create full HTML article page from markdown content"""
    
    # Convert markdown to HTML
    try:
        body_html = markdown.markdown(content, extensions=['extra'])
    except:
        # Fallback simple conversion
        body_html = simple_markdown_to_html(content)
    
    html_template = f"""<!DOCTYPE html>
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
            <span class="category">{category}</span>
            <span class="date">{date}</span>
            <span class="read-time">{read_time}</span>
        </div>
        <div class="article-content">
            {body_html}
        </div>
        <div class="article-footer">
            <a href="index.html" class="btn btn-primary">Back to Journal</a>
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def simple_markdown_to_html(md_text):
    """Simple markdown to HTML fallback conversion"""
    import re
    
    # Convert headers
    md_text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    
    # Convert bold
    md_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_text)
    
    # Convert italic
    md_text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md_text)
    
    # Convert bullet lists
    lines = md_text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if line.strip():
                result.append(f'<p>{line}</p>')
            else:
                result.append('')
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def main():
    """Main execution"""
    print("=" * 60)
    print("THE LONGEVITY JOURNAL - CONVERT ARTICLES TO HTML")
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    for article in ARTICLES:
        # Read the article markdown
        article_path = WEBSITE_DIR / article["file"]
        
        if not article_path.exists():
            print(f"ERROR: {article['file']} not found!")
            continue
        
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        word_count = len(content.split())
        print(f"\n📄 {article['topic']}: {len(content)} chars, ~{word_count} words")
        
        # Create HTML
        article_html = create_article_html(
            content, 
            article["title"], 
            article["topic"],
            article["category"],
            article["read_time"],
            article["date"]
        )
        
        # Save article
        article_filename = f"{article['topic']}-20260529.html"
        output_path = WEBSITE_DIR / article_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(article_html)
        
        print(f"✅ Saved: {output_path}")
        print(f"📊 Size: {output_path.stat().st_size / 1024:.1f} KB")
    
    print("\n" + "=" * 60)
    print("ALL ARTICLES CONVERTED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
