import markdown
import sys
import re
from pathlib import Path

# Configure stdout for UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def convert_article(md_file, html_file, title, category, read_time, color):
    # Read markdown
    md_content = Path(md_file).read_text(encoding='utf-8')
    
    # Convert to HTML
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    html_body = md.convert(md_content)
    
    # Read template from existing article
    template = Path('senolytics-20260529.html').read_text(encoding='utf-8')
    
    # Extract header (before article-header div)
    header_match = re.search(r'(.*?)(\s*<div class="article-header">)', template, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    
    # Extract footer (after closing article tag)
    footer_match = re.search(r'(</article>.*)', template, re.DOTALL)
    footer = footer_match.group(1) if footer_match else ''
    
    # Build article header section
    article_header = f'''
    <div class="article-page container">
        <a href="index.html" class="back-link">← Back to Latest Issue</a>
        
        <div class="article-header">
            <div class="article-tag" style="background: {color};">{category}</div>
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
                <span class="meta-item">📅 May 29, 2026</span>
                <span class="meta-item">⏱️ {read_time} min read</span>
                <span class="meta-item">🔬 Research Review</span>
            </div>
        </div>
        
        <article class="article-body">
'''
    
    # Combine everything
    full_html = header + article_header + html_body + '\n        </article>' + footer
    
    # Write output
    Path(html_file).write_text(full_html, encoding='utf-8')
    
    size_kb = len(full_html) / 1024
    print(f"✅ Created {html_file} ({size_kb:.1f} KB)")
    return size_kb

# Convert all 4 new articles
articles = [
    ('apoe4_article.md', 'apoe4-20260529.html', 
     'APOE4 Carriers: The Alzheimer\'s Gene Isn\'t a Death Sentence', 
     'Genetics', '8', '#E74C3C'),
    ('sleep_article.md', 'sleep-optimization-20260529.html',
     'Sleep Optimization: The Most Underrated Longevity Intervention',
     'Sleep', '10', '#9B59B6'),
    ('ai_drug_article.md', 'ai-drug-discovery-20260529.html',
     'AI Drug Discovery: How Machine Learning Is Finding New Longevity Compounds',
     'Technology', '9', '#34495E'),
    ('trt_article.md', 'trt-longevity-20260529.html',
     'Testosterone Replacement Therapy: Benefits, Risks, and the Longevity Debate',
     'Hormones', '11', '#D35400')
]

for md_file, html_file, title, category, read_time, color in articles:
    if Path(md_file).exists():
        convert_article(md_file, html_file, title, category, read_time, color)
    else:
        print(f"❌ Missing: {md_file}")

print("\n🎉 All articles converted!")
