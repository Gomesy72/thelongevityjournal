#!/usr/bin/env python3
"""
Research Agent for The Longevity Journal
Scans multiple sources for new longevity research
"""

import requests
import json
import feedparser
from datetime import datetime, timedelta
from pathlib import Path

# Config
OUTPUT_DIR = Path(__file__).parent / ".." / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Sources to scan
SOURCES = {
    "pubmed": "https://pubmed.ncbi.nlm.nih.gov/rss/search/1nA-_JrnxfXdMFs6aN3F1wXbV8/?limit=15&utm_campaign=pubmed-2&fc=20231201000000",
    "biorxiv": "https://connect.biorxiv.org/biorxiv_xml.php?subject=gerontology",
    "longevity_tech": "https://www.longevity.technology/feed/",
}

class ResearchAgent:
    def __init__(self):
        self.findings = []
        self.log(f"Research Agent started at {datetime.now()}")
    
    def log(self, message):
        print(f"[RESEARCH] {message}")
    
    def scan_pubmed(self):
        """Scan PubMed RSS feed for new longevity papers"""
        try:
            feed = feedparser.parse(SOURCES["pubmed"])
            for entry in feed.entries[:5]:
                paper = {
                    "source": "pubmed",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get("published", "unknown"),
                    "summary": entry.get("summary", "")[:300],
                    "relevance_score": self.score_relevance(entry.title, entry.get("summary", ""))
                }
                if paper["relevance_score"] > 0.6:
                    self.findings.append(paper)
                    self.log(f"Found: {paper['title'][:80]}... (score: {paper['relevance_score']:.2f})")
        except Exception as e:
            self.log(f"PubMed error: {e}")
    
    def scan_biorxiv(self):
        """Scan bioRxiv preprints"""
        try:
            feed = feedparser.parse(SOURCES["biorxiv"])
            for entry in feed.entries[:5]:
                paper = {
                    "source": "biorxiv",
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.get("published", "unknown"),
                    "summary": entry.get("summary", "")[:300],
                    "relevance_score": self.score_relevance(entry.title, entry.get("summary", ""))
                }
                if paper["relevance_score"] > 0.7:
                    self.findings.append(paper)
                    self.log(f"Found preprint: {paper['title'][:80]}... (score: {paper['relevance_score']:.2f})")
        except Exception as e:
            self.log(f"bioRxiv error: {e}")
    
    def score_relevance(self, title, summary):
        """Score how relevant a paper is to longevity"""
        keywords = [
            "aging", "longevity", "lifespan", "senescence", "autophagy",
            "nad+", "rapamycin", "metformin", "sirtuin", "telomere",
            "mitochondria", "epigenetic", "biological age", "healthspan",
            "calorie restriction", "intermittent fasting", "resveratrol"
        ]
        text = (title + " " + summary).lower()
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 0.15
        return min(score, 1.0)
    
    def save_findings(self):
        """Save findings for Analysis Agent"""
        output_file = OUTPUT_DIR / f"research_findings_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_found": len(self.findings),
                "findings": sorted(self.findings, key=lambda x: x["relevance_score"], reverse=True)
            }, f, indent=2)
        self.log(f"Saved {len(self.findings)} findings to {output_file}")
        return output_file
    
    def run(self):
        """Main execution"""
        self.log("Scanning sources...")
        self.scan_pubmed()
        self.scan_biorxiv()
        
        if self.findings:
            output_file = self.save_findings()
            self.log(f"Research complete. Found {len(self.findings)} article-worthy papers.")
            return output_file
        else:
            self.log("No new findings today.")
            return None

if __name__ == "__main__":
    agent = ResearchAgent()
    agent.run()
