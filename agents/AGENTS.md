# The Longevity Journal - AI Agent System

## Overview

6 AI agents work together to research, write, fact-check, and publish longevity articles automatically.

## Agent Architecture

```
&nbsp;                  &nbsp;                  &nbsp;                  &nbsp;
Research Agent -> Analysis Agent -> Writer Agent -> Editor Agent
&nbsp;                  &nbsp;                  &nbsp;                  &nbsp;         |
&nbsp;                  &nbsp;                  &nbsp;                  &nbsp;         v
&nbsp;                  &nbsp;                  &nbsp;            Fact-Check Agent
&nbsp;                  &nbsp;                  &nbsp;                  &nbsp;         |
&nbsp;                  &nbsp;                  &nbsp;                  &nbsp;         v
&nbsp;                  &nbsp;                  &nbsp;         Publish Agent (HTML + email)
```

## Agent Roles

### 1. Research Agent
- **Purpose:** Scans 200+ sources daily for new longevity research
- **Sources:** PubMed, bioRxiv, Longevity Technology, Fight Aging!, Bryan Johnson's Blueprint
- **Frequency:** Every 6 hours
- **Output:** JSON feed of new studies with relevance scores

### 2. Analysis Agent
- **Purpose:** Evaluates study quality and newsworthiness
- **Checks:** Sample size, p-values, funding sources, replication status
- **Output:** Ranked list of "article-worthy" studies

### 3. Writer Agent
- **Purpose:** Translates research into readable 2000+ word articles
- **Style:** Evidence-based, cautious claims, actionable takeaways
- **Output:** Markdown draft with citations

### 4. Editor Agent
- **Purpose:** Improves readability, checks tone, ensures consistency
- **Checks:** Reading level (target: 10th grade), flow, engagement
- **Output:** Polished article ready for fact-checking

### 5. Fact-Check Agent
- **Purpose:** Cross-references all claims against primary sources
- **Checks:** Quote accuracy, data verification, citation validity
- **Output:** Fact-check report + approved article

### 6. Publish Agent
- **Purpose:** Converts to HTML, deploys to GitHub Pages, sends newsletter
- **Frequency:** Once approved article is ready
- **Output:** Live website + email to subscribers

## Content Calendar (Weekly)

| Day | Agent Activity |
|---|---|
| Monday | Research Agent scans; Analysis Agent ranks |
| Tuesday | Writer Agent drafts top 3 topics |
| Wednesday | Editor Agent polishes; Fact-Check Agent verifies |
| Thursday | Publish Agent deploys + sends newsletter |
| Friday | Research Agent continues scanning |
| Weekend | Monitoring + trending topic detection |

## Implementation

Each agent is a Python script that can be run:
- Manually: `python agent_research.py`
- Scheduled: Windows Task Scheduler or cron
- Triggered: By completion of previous agent

## Cost

- **AI Model:** Uses your existing Ollama setup (free)
- **Hosting:** GitHub Pages (free)
- **Email:** ConvertKit free tier (up to 1,000 subscribers)
- **Total:** $0/month until you exceed free tiers
