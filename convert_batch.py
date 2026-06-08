import markdown
import sys
from datetime import datetime
from pathlib import Path

# Fix Unicode encoding for Windows
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent
WEBSITE_DIR = BASE_DIR

# 10 new articles to convert
ARTICLES = [
    {"file": "rapamycin.md", "topic": "rapamycin", "title": "Rapamycin: The Molecule That Slows Aging at Its Source", "category": "Pharmaceuticals", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "nad-boosters.md", "topic": "nad-boosters", "title": "NAD+ Boosters: Fueling Cellular Energy for Longevity", "category": "Supplements", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "fasting-protocols.md", "topic": "fasting-protocols", "title": "Fasting Protocols: Ancient Practice Meets Modern Longevity Science", "category": "Lifestyle", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "senolytics.md", "topic": "senolytics", "title": "Senolytics: Clearing Zombie Cells to Reclaim Youth", "category": "Pharmaceuticals", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "metformin.md", "topic": "metformin", "title": "Metformin: The Diabetes Drug That May Slow Aging", "category": "Pharmaceuticals", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "omega-3.md", "topic": "omega-3", "title": "Omega-3 Fatty Acids: Essential Fats for Longevity", "category": "Nutrition", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "sleep-optimization.md", "topic": "sleep-optimization", "title": "Sleep Optimization: The Forgotten Pillar of Longevity", "category": "Lifestyle", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "zone-2-cardio.md", "topic": "zone-2-cardio", "title": "Zone 2 Cardio: The Longevity Exercise Prescription", "category": "Exercise", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "spermidine.md", "topic": "spermidine", "title": "Spermidine: The Polyamine Powering Cellular Renewal", "category": "Supplements", "read_time": "12 min read", "date": "June 9, 2026"},
    {"file": "epigenetic-reprogramming.md", "topic": "epigenetic-reprogramming", "title": "Epigenetic Reprogramming: Rewriting the Code of Aging", "category": "Research", "read_time": "12 min read", "date": "June 9, 2026"},
]

def create_article_html(content, title, topic, category, read_time, date):
    try:
        body_html = markdown.markdown(content, extensions=['extra', 'toc', 'tables', 'fenced_code'])
    except Exception:
        body_html = markdown.markdown(content)

    # Extract first paragraph for meta description
    first_p = ""
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('*') and not line.startswith('-') and not line.startswith('>'):
            first_p = line[:160]
            break

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{first_p}...">
    <title>{title} - The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="site-nav">
        <div class="nav-brand">
            <a href="index.html">The Longevity Journal</a>
        </div>
        <div class="nav-links">
            <a href="index.html">Home</a>
            <a href="archive.html">Archive</a>
            <a href="medical-disclaimer.html">Disclaimer</a>
        </div>
    </nav>
    <article class="article-page">
        <header class="article-header">
            <div class="article-meta-bar">
                <span class="category">{category}</span>
                <span class="date">{date}</span>
                <span class="read-time">{read_time}</span>
            </div>
            <h1>{title}</h1>
        </header>
        <div class="article-content">
            {body_html}
        </div>
        <footer class="article-footer">
            <hr>
            <div class="article-tags">
                <span class="tag">{category}</span>
                <span class="tag">Longevity</span>
                <span class="tag">Research</span>
            </div>
            <div class="article-nav">
                <a href="index.html" class="btn btn-primary">← Back to Journal</a>
                <a href="medical-disclaimer.html" class="btn btn-secondary">Medical Disclaimer</a>
            </div>
        </footer>
    </article>
    <footer class="site-footer">
        <p>&copy; 2026 The Longevity Journal. All content is for informational purposes only and does not constitute medical advice.</p>
    </footer>
</body>
</html>"""
    return html_template

def main():
    print("=" * 60)
    print("THE LONGEVITY JOURNAL - BATCH CONVERT TO HTML")
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    converted = []
    for article in ARTICLES:
        article_path = WEBSITE_DIR / article["file"]
        if not article_path.exists():
            print(f"ERROR: {article['file']} not found!")
            continue

        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        word_count = len(content.split())
        print(f"\n📄 {article['topic']}: {len(content)} chars, ~{word_count} words")

        article_html = create_article_html(
            content, article["title"], article["topic"],
            article["category"], article["read_time"], article["date"]
        )

        output_filename = f"{article['topic']}-20260609.html"
        output_path = WEBSITE_DIR / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(article_html)

        converted.append({"topic": article["topic"], "file": output_filename, "title": article["title"], "category": article["category"]})
        print(f"✅ Saved: {output_path}")
        print(f"📊 Size: {output_path.stat().st_size / 1024:.1f} KB")

    # Write manifest for index generator
    manifest_path = WEBSITE_DIR / "articles_manifest.json"
    import json
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(converted, f, indent=2)
    print(f"\n📋 Manifest saved: {manifest_path}")

    print("\n" + "=" * 60)
    print(f"ALL {len(converted)} ARTICLES CONVERTED!")
    print("=" * 60)
    return converted

if __name__ == "__main__":
    main()
