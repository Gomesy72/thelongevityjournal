#!/usr/bin/env python3
"""
Master Orchestrator for The Longevity Journal
Runs all agents in sequence to generate and publish articles
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

AGENTS_DIR = Path(__file__).parent

def run_agent(script_name, *args):
    """Run an agent script"""
    script_path = AGENTS_DIR / script_name
    if not script_path.exists():
        print(f"[ORCHESTRATOR] ERROR: {script_name} not found")
        return False
    
    print(f"[ORCHESTRATOR] Running {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + list(args),
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ORCHESTRATOR] WARNING: {script_name} returned code {result.returncode}")
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[ORCHESTRATOR] TIMEOUT: {script_name}")
        return False
    except Exception as e:
        print(f"[ORCHESTRATOR] ERROR running {script_name}: {e}")
        return False

def main():
    print("=" * 60)
    print("The Longevity Journal - Agent Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Research
    if not run_agent("agent_research.py"):
        print("[ORCHESTRATOR] Research failed. Stopping pipeline.")
        return
    
    # Step 2: Write (would read research output)
    print("\n[ORCHESTRATOR] Step 2: Writing articles...")
    # In production: run_agent("agent_writer.py", "latest_research.json")
    print("[ORCHESTRATOR] Writer agent ready (connect Ollama model for full generation)")
    
    # Step 3: Publish
    print("\n[ORCHESTRATOR] Step 3: Publishing...")
    print("[ORCHESTRATOR] Publish agent ready (deploy to GitHub Pages)")
    
    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Connect Ollama model (kimi-k2.6:cloud) for article generation")
    print("2. Set up ConvertKit for newsletter delivery")
    print("3. Schedule this script to run weekly via Task Scheduler")

if __name__ == "__main__":
    main()
