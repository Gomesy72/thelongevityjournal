import requests
import json
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

# Ollama API endpoint (local)
OLLAMA_URL = "http://localhost:11434/api/generate"

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

def generate_article_api(topic):
    """Generate article using Ollama API"""
    
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

Write ONLY the article content. No meta-commentary, no "Here's the article:" prefix."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "gemma4:31b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 4000
                }
            },
            timeout=600
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        print(f"Error generating article: {e}")
        return None

def markdown_to_html(markdown_text):
    """Simple markdown to HTML conversion"""
    lines = markdown_text.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Headers
        if stripped.startswith('# '):
            html_lines.append(f'<h1>{html.escape(stripped[2:])}</h1>')
        elif stripped.startswith('## '):
            html_lines.append(f'<h2>{html.escape(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            html_lines.append(f'<h3>{html.escape(stripped[4:])}</h3>')
        # Bullet points
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{html.escape(stripped[2:])}</li>')
        # Numbered lists
        elif stripped and stripped[0].isdigit() and '. ' in stripped[:3]:
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            content = stripped[stripped.find('. ')+2:]
            html_lines.append(f'<li>{html.escape(content)}</li>')
        # Empty line
        elif not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
        # Regular paragraph
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{html.escape(stripped)}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def create_article_html(content, title, topic):
    """Create full HTML article page"""
    
    body_html = markdown_to_html(content)
    
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
            <span class="category">Research</span>
            <span class="date">{datetime.now().strftime('%B %d, %Y')}</span>
            <span class="read-time">8 min read</span>
        </div>
        <div class="article-content">
            {body_html}
        </div>
        <div class="article-footer">
            <a href="index.html" class="btn btn-primary">← Back to Journal</a>
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def update_index_html(article_filename, title, topic):
    """Add new article card to index.html"""
    
    index_path = WEBSITE_DIR / "index.html"
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create article card HTML
        date_str = datetime.now().strftime('%B %d, %Y')
        card_html = f'''        <div class="article-card">
            <div class="article-image">
                <div class="placeholder-img" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <span>{topic.replace('-', ' ').title()[:1]}</span>
                </div>
            </div>
            <div class="article-content">
                <div class="article-meta">
                    <span class="category">Research</span>
                    <span class="date">{date_str}</span>
                </div>
                <h3>{title}</h3>
                <p>Latest evidence on {topic.replace('-', ' ')} and its impact on longevity.</p>
                <a href="{article_filename}" class="read-more">Read More →</a>
            </div>
        </div>
'''
        
        # Find the articles grid and insert after the opening div
        if '<div class="articles-grid">' in content:
            insert_point = content.find('<div class="articles-grid">') + len('<div class="articles-grid">')
            content = content[:insert_point] + '\n' + card_html + content[insert_point:]
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated index.html with new article card")
            return True
        else:
            print("⚠️ Could not find articles-grid in index.html")
            return False
            
    except Exception as e:
        print(f"❌ Error updating index.html: {e}")
        return False

def deploy_to_github():
    """Deploy changes to GitHub"""
    import subprocess
    
    try:
        # Check if git repo
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=WEBSITE_DIR,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("ℹ️ No changes to deploy")
            return True
        
        # Add, commit, push
        subprocess.run(["git", "add", "."], cwd=WEBSITE_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Add article: {datetime.now().strftime('%Y-%m-%d')}"],
            cwd=WEBSITE_DIR,
            check=True
        )
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=WEBSITE_DIR,
            check=True
        )
        
        print("✅ Deployed to GitHub successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Deploy failed: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("THE LONGEVITY JOURNAL - ARTICLE GENERATOR")
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Determine topic (weekly rotation)
    week_number = datetime.now().isocalendar()[1]
    topic = TOPICS[week_number % len(TOPICS)]
    title = f"The Science of {topic.replace('-', ' ').title()}"
    
    print(f"\n📄 Topic: {topic}")
    print(f"📝 Title: {title}")
    
    # Step 1: Generate article
    print("\n⏳ Generating article via Ollama API...")
    print("   (This may take 2-5 minutes...)")
    
    article_content = generate_article_api(topic)
    
    if not article_content:
        print("❌ FAILED: Article generation failed")
        return False
    
    content_length = len(article_content)
    word_count = len(article_content.split())
    print(f"✅ Article generated: {content_length} chars, ~{word_count} words")
    
    if word_count < 500:
        print("⚠️ WARNING: Article seems too short. Content:")
        print(article_content[:500])
        return False
    
    # Step 2: Create HTML
    print("\n🎨 Converting to HTML...")
    article_html = create_article_html(article_content, title, topic)
    
    # Step 3: Save article
    article_filename = f"{topic}-{datetime.now().strftime('%Y%m%d')}.html"
    article_path = WEBSITE_DIR / article_filename
    
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(article_html)
    
    print(f"✅ Saved: {article_path}")
    print(f"📊 Size: {article_path.stat().st_size / 1024:.1f} KB")
    
    # Step 4: Update index
    print("\n🌐 Updating website index...")
    update_index_html(article_filename, title, topic)
    
    # Step 5: Deploy
    print("\n🚀 Deploying to GitHub...")
    deploy_to_github()
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE!")
    print(f"📖 Article: {article_filename}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
