#!/usr/bin/env python3
"""
Writer Agent for The Longevity Journal
Generates full HTML articles from research summaries
"""

import json
from datetime import datetime
from pathlib import Path

TEMPLATE = """{html_content}"""

class WriterAgent:
    def __init__(self):
        self.log(f"Writer Agent started")
    
    def log(self, message):
        print(f"[WRITER] {message}")
    
    def generate_article(self, topic, sources, word_count=2000):
        """Generate a full article from research data
        
        In production, this would call your Ollama model:
        - model: ollama/kimi-k2.6:cloud
        - prompt: Write a {word_count}-word article on {topic}
        - style: Evidence-based, cautious claims, actionable
        """
        self.log(f"Generating article: {topic}")
        
        # Article structure template
        article = {
            "title": topic,
            "category": self.categorize_topic(topic),
            "read_time": f"{word_count // 250} min read",
            "word_count": word_count,
            "sources_count": len(sources),
            "status": "draft"
        }
        
        self.log(f"Article draft created: {article['title']}")
        self.log(f"To complete: Connect to your Ollama model for full content generation")
        
        return article
    
    def categorize_topic(self, topic):
        """Categorize article by topic"""
        topic_lower = topic.lower()
        categories = {
            "supplements": ["nad+", "nmn", "nr", "niacin", "resveratrol", "spermidine", "rapamycin"],
            "nutrition": ["diet", "fasting", "keto", "protein", "calorie"],
            "exercise": ["cardio", "hiit", "strength", "zone 2", "workout"],
            "sleep": ["sleep", "circadian", "melatonin"],
            "biohacking": ["epigenetic", "biological age", "clock", "dna methylation"],
            "tech": ["ai", "drug discovery", "gene therapy", "crispr"]
        }
        
        for category, keywords in categories.items():
            if any(kw in topic_lower for kw in keywords):
                return category
        return "general"
    
    def run(self, research_file=None):
        """Main execution - reads research output and writes articles"""
        if research_file and Path(research_file).exists():
            with open(research_file, 'r') as f:
                data = json.load(f)
            
            self.log(f"Processing {data['total_found']} findings...")
            
            articles = []
            for finding in data["findings"][:3]:  # Top 3 topics
                article = self.generate_article(
                    topic=finding["title"],
                    sources=[finding["url"]],
                    word_count=2000
                )
                articles.append(article)
            
            self.log(f"Generated {len(articles)} article drafts")
            return articles
        else:
            self.log("No research file provided. Using demo mode.")
            demo_article = self.generate_article(
                topic="Demo: New Longevity Research",
                sources=["https://example.com"],
                word_count=2000
            )
            return [demo_article]

if __name__ == "__main__":
    agent = WriterAgent()
    articles = agent.run()
    print(f"\nGenerated {len(articles)} article drafts")
    for a in articles:
        print(f"  - {a['title']} ({a['category']}, {a['read_time']})")
