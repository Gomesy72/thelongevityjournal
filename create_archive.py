import os
from datetime import datetime

os.chdir("C:\\Openclaw\\agents\\longevity-journal")

# Get all article HTML files (only content articles, not system pages)
articles = []
for f in os.listdir('.'):
    if f.endswith('.html') and f not in ['index.html', 'archive.html'] and not any(x in f for x in ['welcome', 'newsletter', 'terms', 'privacy', 'medical', 'confirmed']):
        stat = os.stat(f)
        articles.append({
            'file': f,
            'date': datetime.fromtimestamp(stat.st_mtime),
            'size': stat.st_size
        })

# Sort by date (newest first)
articles.sort(key=lambda x: x['date'], reverse=True)

# Map filenames to titles
titles = {
    'senolytics-20260529.html': 'Senolytics: The Science of Clearing Zombie Cells',
    'rapamycin-20260529.html': 'Rapamycin: Extending Lifespan with a Single Pill',
    'nad-boosters-20260529.html': 'NAD+ Supplements: The Science Behind Cellular Energy',
    'nad-supplements-20260529.html': 'NAD+ Supplements: The Science Behind Cellular Energy',
    'zone2-cardio-20260529.html': 'Zone 2 Training: The Longevity Exercise Protocol',
    'zone2-training-20260529.html': 'Zone 2 Training: The Longevity Exercise Protocol',
    'apoe4-20260529.html': 'APOE4 Gene: What It Means for Alzheimer\'s Risk',
    'sleep-optimization-20260529.html': 'The Science of Sleep Optimization',
    'ai-drug-discovery-20260529.html': 'AI-Designed Drug Targets Aging at the Cellular Level',
    'trt-longevity-20260529.html': 'Testosterone Replacement Therapy: A Longevity Perspective'
}

# Create archive HTML
archive_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive | The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .archive-item { padding: 1rem 0; border-bottom: 1px solid #e0e0e0; }
        .archive-date { color: #666; font-size: 0.9rem; display: block; margin-bottom: 0.3rem; }
        .archive-link { font-weight: 600; color: #1a3c6c; text-decoration: none; font-size: 1.1rem; }
        .archive-link:hover { text-decoration: underline; }
        .archive-tag { background: #1a3c6c; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem; }
        .archive-count { color: #666; font-style: italic; margin-bottom: 2rem; }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo">The Longevity Journal</div>
            <nav>
                <a href="index.html">Home</a>
                <a href="archive.html">Archive</a>
            </nav>
        </div>
    </header>

    <div class="container">
        <article class="article-page">
            <a href="index.html" class="back-link">&larr; Back to Journal</a>
            
            <h1>Article Archive</h1>
            <p class="archive-count">""" + str(len(articles)) + """ articles available</p>
            <p class="lead">Complete collection of longevity research articles. All articles are fact-checked and sourced from peer-reviewed studies.</p>

            <h2>All Articles</h2>
"""

for article in articles:
    title = titles.get(article['file'], article['file'].replace('-', ' ').replace('.html', ''))
    date_str = article['date'].strftime("%B %d, %Y")
    
    archive_html += f"""
            <div class="archive-item">
                <span class="archive-date">{date_str}</span>
                <a href="{article['file']}" class="archive-link">{title}</a>
                <span class="archive-tag">Research</span>
            </div>
"""

archive_html += """
        </article>
    </div>

    <footer>
        <p>&copy; 2026 The Longevity Journal. All rights reserved.</p>
    </footer>
</body>
</html>
"""

with open('archive.html', 'w', encoding='utf-8') as f:
    f.write(archive_html)

print("Archive page created successfully!")
print(f"Total articles: {len(articles)}")
for a in articles:
    print(f"  - {a['file']}: {titles.get(a['file'], 'Unknown')}")
