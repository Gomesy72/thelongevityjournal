import re
import os

def md_to_html_clean(title, md_file, html_file):
    """Convert markdown to HTML with only ASCII-safe characters"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Replace special characters with ASCII equivalents or HTML entities
    md_content = md_content.replace('—', '--')  # em dash -> double hyphen
    md_content = md_content.replace('–', '-')   # en dash -> hyphen
    md_content = md_content.replace('"', '&quot;')  # left double quote
    md_content = md_content.replace('"', '&quot;')  # right double quote
    md_content = md_content.replace(''','\'')   # left single quote
    md_content = md_content.replace(''','\'')   # right single quote/apostrophe
    md_content = md_content.replace('…', '...')  # ellipsis -> three dots
    md_content = md_content.replace('←', '&lt;-')  # left arrow
    md_content = md_content.replace('→', '-&gt;')  # right arrow
    md_content = md_content.replace('·', '&middot;')  # middle dot
    md_content = md_content.replace('•', '*')   # bullet -> asterisk
    
    # Simple markdown to HTML conversion
    lines = md_content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
            continue
            
        # Headers
        if line.startswith('# '):
            text = line[2:]
            html_lines.append(f'<h1>{text}</h1>')
        elif line.startswith('## '):
            text = line[3:]
            html_lines.append(f'<h2>{text}</h2>')
        elif line.startswith('### '):
            text = line[4:]
            html_lines.append(f'<h3>{text}</h3>')
        elif line.startswith('---'):
            html_lines.append('<hr>')
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = line[2:]
            # Handle bold in list items
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
            html_lines.append(f'<li>{text}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # Handle bold and italic
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    body_content = '\n'.join(html_lines)
    
    # Build complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&amp;display=swap" rel="stylesheet">
</head>
<body>

    <!-- Noise Texture Overlay -->
    <div class="noise-overlay"></div>

    <header class="masthead">
        <div class="container">
            <div class="masthead-inner">
                <div class="masthead-left">
                    <span class="masthead-date">May 29, 2026</span>
                    <span class="masthead-issue">Issue No. 001</span>
                </div>
                <div class="masthead-center">
                    <div class="masthead-logo">TLJ</div>
                    <h1 class="masthead-title">The Longevity Journal</h1>
                    <div class="masthead-tagline">AI-Curated Research &middot; Human-Tested</div>
                </div>
                <div class="masthead-right">
                    <a href="index.html#newsletter" class="btn-subscribe">Subscribe Free -&gt;</a>
                </div>
            </div>
        </div>
    </header>

    <nav class="site-nav">
        <div class="container">
            <div class="site-nav-inner">
                <a href="index.html">Home</a>
                <a href="index.html#articles">Articles</a>
                <a href="index.html#about">About</a>
                <a href="index.html#newsletter">Subscribe</a>
            </div>
        </div>
    </nav>

    <div class="article-page container">
        <a href="index.html" class="back-link">&lt;- Back to Latest Issue</a>
        
        <div class="article-header">
            <span class="article-tag">Genetics</span>
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
                <span>May 29, 2026</span>
                <span>8 min read</span>
                <span>Research Review</span>
            </div>
        </div>
        
        <div class="article-content">
            <article class="article-body">
                {body_content}
            </article>
        </div>
    </div>
</body>
</html>'''
    
    # Write without BOM
    with open(html_file, 'w', encoding='utf-8-sig') as f:
        f.write(html)
    
    # Remove BOM that utf-8-sig adds
    with open(html_file, 'rb') as f:
        content = f.read()
    
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    
    with open(html_file, 'wb') as f:
        f.write(content)
    
    print(f"Created {html_file}")

# Create all 4 articles
articles = [
    ('APOE4 Carriers: The Alzheimer\'s Gene Isn\'t a Death Sentence', 'apoe4_article.md', 'apoe4-20260529.html'),
    ('Sleep Optimization: The Most Underrated Longevity Intervention', 'sleep_article.md', 'sleep-optimization-20260529.html'),
    ('AI Drug Discovery: How Machine Learning Is Finding New Longevity Compounds', 'ai_drug_article.md', 'ai-drug-discovery-20260529.html'),
    ('Testosterone Replacement Therapy: Benefits, Risks, and the Longevity Debate', 'trt_article.md', 'trt-longevity-20260529.html'),
]

for title, md, html in articles:
    if os.path.exists(md):
        md_to_html_clean(title, md, html)
    else:
        print(f"Missing {md}")

print("\nAll articles recreated with clean ASCII!")
