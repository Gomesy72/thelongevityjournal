import os
import re
import shutil

# First, let's create a simple ASCII-only markdown to HTML converter
def clean_text(text):
    """Replace special characters with ASCII equivalents"""
    replacements = {
        '—': '--',
        '–': '-',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
        '←': '&lt;-',
        '→': '-&gt;',
        '·': '&middot;',
        '•': '*',
        '–': '-',
        '—': '--',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def md_to_html(title, md_content, output_file):
    """Convert markdown to clean HTML"""
    
    # Clean the markdown content
    md_content = clean_text(md_content)
    
    # Simple markdown parsing
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
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
            html_lines.append(f'<li>{text}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    body_content = '\n'.join(html_lines)
    
    # Build HTML with ASCII-only characters
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
            <span class="article-tag">Research</span>
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
                <span>May 29, 2026</span>
                <span>10 min read</span>
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
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Verify no BOM
    with open(output_file, 'rb') as f:
        content = f.read()
    if content.startswith(b'\xef\xbb\xbf'):
        with open(output_file, 'wb') as f:
            f.write(content[3:])
    
    print(f"Created {output_file}")

# Check if markdown source files exist
md_files = {
    'apoe4_article.md': ('APOE4 Carriers: The Alzheimer\'s Gene Isn\'t a Death Sentence', 'apoe4-20260529.html'),
    'sleep_article.md': ('Sleep Optimization: The Most Underrated Longevity Intervention', 'sleep-optimization-20260529.html'),
    'ai_drug_article.md': ('AI Drug Discovery: How Machine Learning Is Finding New Longevity Compounds', 'ai-drug-discovery-20260529.html'),
    'trt_article.md': ('Testosterone Replacement Therapy: Benefits, Risks, and the Longevity Debate', 'trt-longevity-20260529.html'),
    'senolytics_article.md': ('The Science of Senolytics: Can Clearing Zombie Cells Extend Healthy Lifespan?', 'senolytics-20260529.html'),
    'rapamycin_article.md': ('Rapamycin: The Anti-Aging Drug From Easter Island', 'rapamycin-20260529.html'),
    'nad_boosters_article.md': ('NAD+ Boosters: NMN vs NR vs Niacin', 'nad-boosters-20260529.html'),
    'zone2_article.md': ('Zone 2 Cardio: The Exercise Prescription for Longevity', 'zone2-cardio-20260529.html'),
}

for md_file, (title, html_file) in md_files.items():
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        md_to_html(title, md_content, html_file)
    else:
        print(f"Missing {md_file}")

print("\nAll articles recreated with clean ASCII!")
