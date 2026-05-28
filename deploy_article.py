import markdown
import html
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
WEBSITE_DIR = BASE_DIR

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

def create_article_html(markdown_content, title, topic):
    """Create full HTML article page from markdown content"""
    
    # Convert markdown to HTML
    try:
        body_html = markdown.markdown(markdown_content, extensions=['extra'])
    except:
        # Fallback simple conversion
        body_html = simple_markdown_to_html(markdown_content)
    
    date_str = datetime.now().strftime('%B %d, %Y')
    
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
            <span class="date">{date_str}</span>
            <span class="read-time">10 min read</span>
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

def update_index_html(article_filename, title, topic):
    """Add new article card to index.html"""
    
    index_path = WEBSITE_DIR / "index.html"
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create article card HTML - matching existing article-card structure
        date_str = datetime.now().strftime('%B %d, %Y')
        card_html = f'''                <article class="article-card" data-category="supplements">
                    <div class="card-label">Research</div>
                    <h3 class="card-title">{title}</h3>
                    <p class="card-excerpt">Latest evidence on senolytics and their impact on longevity. Can clearing 'zombie cells' extend healthy lifespan?</p>
                    <div class="card-meta">
                        <span>10 min read &middot; {date_str}</span>
                        <a href="{article_filename}" class="card-link">Read &rarr;</a>
                    </div>
                </article>
'''
        
        # Find the articles grid and insert after the opening div
        if '<div class="article-grid">' in content:
            insert_point = content.find('<div class="article-grid">') + len('<div class="article-grid">')
            content = content[:insert_point] + '\n' + card_html + content[insert_point:]
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("Updated index.html with new article card")
            return True
        else:
            print("Could not find article-grid in index.html")
            return False
            
    except Exception as e:
        print(f"Error updating index.html: {e}")
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
            print("No changes to deploy")
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
        
        print("Deployed to GitHub successfully!")
        return True
        
    except Exception as e:
        print(f"Deploy failed: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("THE LONGEVITY JOURNAL - ARTICLE DEPLOYMENT")
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Read the generated article
    article_path = WEBSITE_DIR / "senolytics_article.md"
    
    if not article_path.exists():
        print("ERROR: senolytics_article.md not found!")
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        article_content = f.read()
    
    word_count = len(article_content.split())
    print(f"Article loaded: {len(article_content)} chars, ~{word_count} words")
    
    # Determine topic
    topic = "senolytics"
    title = "The Science of Senolytics: Can Clearing 'Zombie Cells' Extend Healthy Lifespan?"
    
    # Create HTML
    print("Converting to HTML...")
    article_html = create_article_html(article_content, title, topic)
    
    # Save article
    article_filename = f"{topic}-{datetime.now().strftime('%Y%m%d')}.html"
    output_path = WEBSITE_DIR / article_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(article_html)
    
    print(f"Saved: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Update index
    print("\nUpdating website index...")
    update_index_html(article_filename, title, topic)
    
    # Deploy
    print("\nDeploying to GitHub...")
    deploy_to_github()
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print(f"Article: {article_filename}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
