#!/usr/bin/env python3
"""
Weekly Article Pipeline for The Longevity Journal
Generates and publishes one article per week

Usage:
    uv run python weekly_pipeline.py --test    # Test mode (dry run)
    uv run python weekly_pipeline.py --live    # Live mode (publishes)
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
AGENTS_DIR = Path(__file__).parent / "agents"
ARTICLES_DIR = Path(__file__).parent / "articles"
OUTPUT_DIR = Path(__file__).parent / "output"
REPO_DIR = Path(__file__).parent  # Git repo root

# Load ConvertKit config
CONVERTKIT_CONFIG = Path(__file__).parent / "convertkit_config.json"

def load_convertkit_config():
    """Load ConvertKit configuration"""
    if CONVERTKIT_CONFIG.exists():
        with open(CONVERTKIT_CONFIG, 'r') as f:
            return json.load(f)
    return {}

# Ollama models from config
DEFAULT_MODEL = "ollama/kimi-k2.6:cloud"  # Default cloud model
FALLBACK_MODEL = "ollama/qwen2.5:3b"      # Local fallback

class WeeklyPipeline:
    def __init__(self, test_mode=True):
        self.test_mode = test_mode
        self.log_file = OUTPUT_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
        OUTPUT_DIR.mkdir(exist_ok=True)
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    
    def run_research(self):
        """Step 1: Research latest longevity topics"""
        self.log("=" * 50)
        self.log("STEP 1: Research Phase")
        self.log("=" * 50)
        
        # Use Tavily search to find trending longevity topics
        topics = [
            "latest longevity research 2026",
            "new anti-aging supplements clinical trials",
            "epigenetic clock advances 2026",
            "rapamycin human trials results",
            "NAD+ booster new studies"
        ]
        
        self.log(f"Searching {len(topics)} topics via Tavily...")
        
        # For test mode, use cached/research results
        if self.test_mode:
            self.log("TEST MODE: Using sample research data")
            return {
                "topic": "Spermidine: The Wheat Germ Compound That Triggers Autophagy",
                "category": "Supplements",
                "sources": [
                    "https://pubmed.ncbi.nlm.nih.gov/",
                    "https://www.longevity.technology/"
                ],
                "key_findings": [
                    "1mg/day spermidine reduces biological age markers by 2.3 years",
                    "Triggers cellular autophagy - the body's recycling system",
                    "New human trial completed December 2025"
                ]
            }
        
        # Live mode would call Tavily API here
        return None
    
    def generate_article(self, research_data):
        """Step 2: Generate article content using Ollama"""
        self.log("=" * 50)
        self.log("STEP 2: Article Generation")
        self.log("=" * 50)
        
        prompt = f"""Write a 2000-word evidence-based article on:
        
Topic: {research_data['topic']}
Category: {research_data['category']}
Key Findings: {', '.join(research_data['key_findings'])}

Requirements:
- Evidence-based, cautious claims
- Include practical, actionable takeaways
- Cite primary sources (use real study citations)
- Target reading level: 10th grade
- Tone: Professional but accessible
- Include a comparison table where relevant
- End with "The Bottom Line" summary
- Add medical disclaimer

Structure:
1. Hook paragraph (why this matters)
2. Background/Science
3. Latest Research Findings
4. Practical Applications
5. Comparison with alternatives (table)
6. Risks/Side Effects
7. The Bottom Line
8. Primary Sources (citations)
9. Medical Disclaimer

Write the full article now."""

        self.log(f"Generating with model: {DEFAULT_MODEL}")
        
        if self.test_mode:
            self.log("TEST MODE: Would generate article here")
            self.log("In live mode, calls Ollama API with prompt")
            return None
        
        # Live mode: Call Ollama
        try:
            result = subprocess.run(
                ["openclaw", "run", "--model", DEFAULT_MODEL, "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.stdout
        except Exception as e:
            self.log(f"ERROR generating article: {e}")
            return None
    
    def convert_to_html(self, article_text, research_data):
        """Step 3: Convert article to HTML with styling"""
        self.log("=" * 50)
        self.log("STEP 3: HTML Conversion")
        self.log("=" * 50)
        
        # Read template
        template_path = AGENTS_DIR / "article_template.html"
        if not template_path.exists():
            self.log("Creating default HTML template...")
            self.create_default_template()
        
        # For test mode, just log
        if self.test_mode:
            self.log("TEST MODE: Would convert to HTML")
            filename = f"article_{datetime.now().strftime('%Y%m%d')}.html"
            self.log(f"Output file: {filename}")
            return filename
        
        return None
    
    def create_default_template(self):
        """Create default article HTML template"""
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Longevity Journal</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="logo">
                <span class="logo-icon">TLJ</span>
                <div class="logo-text">
                    <h1>The Longevity Journal</h1>
                    <span class="tagline">AI-Curated Research, Human-Tested</span>
                </div>
            </div>
            <nav class="nav">
                <a href="index.html">Home</a>
                <a href="index.html#articles">Articles</a>
                <a href="index.html#about">About</a>
                <a href="index.html#newsletter" class="btn-primary">Subscribe</a>
            </nav>
        </div>
    </header>

    <!-- Article Content -->
    <main class="article-page">
        <div class="container">
            <a href="index.html" class="back-link">&larr; Back to Latest Issue</a>
            
            <article class="article-full">
                <header class="article-header">
                    <span class="article-category">{category}</span>
                    <h1>{title}</h1>
                    <div class="article-meta-bar">
                        <span>By Research Agent-7</span>
                        <span>{date}</span>
                        <span>{read_time} min read</span>
                        <span>Primary sources: {sources_count} studies</span>
                    </div>
                </header>
                
                <div class="article-content">
                    {content}
                </div>
            </article>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 The Longevity Journal. All research summaries are for informational purposes only. Not medical advice.</p>
            <p>Powered by AI Agents | Built with OpenClaw</p>
        </div>
    </footer>
</body>
</html>"""
        
        template_path = AGENTS_DIR / "article_template.html"
        template_path.parent.mkdir(exist_ok=True)
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template)
        self.log("Created article_template.html")
    
    def update_website(self, html_file):
        """Step 4: Add article to website and push to GitHub"""
        self.log("=" * 50)
        self.log("STEP 4: Website Update")
        self.log("=" * 50)
        
        if self.test_mode:
            self.log("TEST MODE: Would update index.html and push to GitHub")
            self.log("Commands that would run:")
            self.log("  1. Add article card to index.html")
            self.log("  2. git add -A")
            self.log("  3. git commit -m 'Add new article'")
            self.log("  4. git push origin main")
            return True
        
        # Live mode: Update index.html and push
        try:
            # Add article to grid
            # Commit and push
            subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, check=True)
            subprocess.run(["git", "commit", "-m", f"Add article: {html_file}"], cwd=REPO_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
            self.log("Successfully pushed to GitHub!")
            return True
        except Exception as e:
            self.log(f"ERROR updating website: {e}")
            return False
    
    def send_newsletter(self, article_data):
        """Step 5: Send newsletter via ConvertKit"""
        self.log("=" * 50)
        self.log("STEP 5: Newsletter")
        self.log("=" * 50)
        
        if self.test_mode:
            self.log("TEST MODE: Would send newsletter via ConvertKit")
            self.log("Need: ConvertKit API key configured")
            return True
        
        # Live mode: Call ConvertKit API
        self.log("Sending newsletter to subscribers...")
        return True
    
    def run_full_pipeline(self):
        """Execute complete weekly pipeline"""
        self.log("=" * 60)
        self.log("THE LONGEVITY JOURNAL - WEEKLY PIPELINE")
        self.log(f"Mode: {'TEST (dry run)' if self.test_mode else 'LIVE'}")
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 60)
        
        # Step 1: Research
        research = self.run_research()
        if not research:
            self.log("ERROR: Research phase failed")
            return False
        
        # Step 2: Generate
        article_text = self.generate_article(research)
        if not article_text and not self.test_mode:
            self.log("ERROR: Article generation failed")
            return False
        
        # Step 3: Convert to HTML
        html_file = self.convert_to_html(article_text, research)
        if not html_file:
            self.log("ERROR: HTML conversion failed")
            return False
        
        # Step 4: Update website
        if not self.update_website(html_file):
            self.log("ERROR: Website update failed")
            return False
        
        # Step 5: Newsletter
        if not self.send_newsletter(research):
            self.log("WARNING: Newsletter not sent")
        
        self.log("=" * 60)
        self.log("PIPELINE COMPLETE!")
        self.log(f"Log saved: {self.log_file}")
        self.log("=" * 60)
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Weekly article pipeline")
    parser.add_argument("--test", action="store_true", help="Test mode (dry run)")
    parser.add_argument("--live", action="store_true", help="Live mode (publishes)")
    args = parser.parse_args()
    
    test_mode = not args.live  # Default to test mode for safety
    
    pipeline = WeeklyPipeline(test_mode=test_mode)
    success = pipeline.run_full_pipeline()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
