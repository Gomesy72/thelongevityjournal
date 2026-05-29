# Fix remaining 3 articles by wrapping them in proper HTML structure

import re

def fix_article(filename, title):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the article content (remove any partial HTML wrapper if present)
    # Find the article content between article-page container div
    match = re.search(r'<div class="article-page container">(.*)</article>', content, re.DOTALL)
    if match:
        article_content = match.group(1)
    else:
        article_content = content
    
    # Build proper HTML structure
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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
                    <a href="index.html#newsletter" class="btn-subscribe">Subscribe Free &rarr;</a>
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
        <a href="index.html" class="back-link">&larr; Back to Latest Issue</a>
        {article_content}
        </article>
    </div>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Fixed {filename}")

# Fix the remaining 3 articles
fix_article('trt-longevity-20260529.html', 'Testosterone Replacement Therapy: Benefits, Risks, and the Longevity Debate')
fix_article('ai-drug-discovery-20260529.html', 'AI Drug Discovery: How Machine Learning Is Finding New Longevity Compounds')
fix_article('apoe4-20260529.html', 'APOE4 Carriers: The Alzheimer\'s Gene Isn\'t a Death Sentence')

print("All articles fixed!")
