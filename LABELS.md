# 🏷️ BrandSynapse AI — Contributor Labels & Project Status Guide

> This document is the **single source of truth** for contributors. It tells you exactly what has been built, what is actively being worked on, what needs help, and how to pick up a task. Read this before opening an issue or submitting a PR.

---

## 📌 How to Use This Document

1. **New contributor?** → Start with [🟢 Good First Issues](#-good-first-issues)
2. **Experienced dev?** → Jump to [🔥 High Priority](#-high-priority--help-wanted)
3. **Researcher / ML engineer?** → Check [🤖 AI & ML Tasks](#-ai--ml-tasks)
4. **Want to see the big picture?** → Read [✅ What's Been Done](#-whats-been-done) and [🗺️ What's Next](#️-whats-next)

When you pick up a task, **comment on the issue** so others know it's taken. Label your PR with the matching label from this guide.

---

## ✅ What's Been Done

*Completed work — stable and merged into `main`.*

| # | Module | Description | Labels |
|---|--------|-------------|--------|
| 1 | **Project Scaffold** | Monorepo structure, Docker Compose setup, CI skeleton | `completed` `infrastructure` |
| 2 | **Data Ingestion — Twitter/X** | Tweepy-based streaming collector with keyword filters | `completed` `ingestion` |
| 3 | **Data Ingestion — Reddit** | PRAW-based subreddit monitor and post collector | `completed` `ingestion` |
| 4 | **Data Ingestion — News** | NewsAPI integration with category and keyword routing | `completed` `ingestion` |
| 5 | **Kafka Pipeline** | Producer/consumer setup, topic partitioning, basic dead-letter queue | `completed` `infrastructure` |
| 6 | **Text Preprocessing** | Cleaning, normalization, language detection, deduplication | `completed` `nlp` |
| 7 | **Basic Sentiment Model** | 3-class BERT-based classifier (positive / neutral / negative) | `completed` `ml` `nlp` |
| 8 | **PostgreSQL Schema** | Core tables: mentions, brands, sentiments, sources | `completed` `database` |
| 9 | **Redis Caching Layer** | Session cache and hot-data TTL caching for API responses | `completed` `infrastructure` |
| 10 | **FastAPI Backend — Core** | Project structure, base router, health endpoint, CORS | `completed` `backend` |
| 11 | **REST API — Mentions** | Endpoints to fetch, filter, and paginate brand mentions | `completed` `backend` |
| 12 | **Basic React Dashboard** | Shell layout, sidebar navigation, placeholder pages | `completed` `frontend` |
| 13 | **Live Sentiment Chart** | Line chart showing sentiment score over time (Chart.js) | `completed` `frontend` |
| 14 | **Docker Multi-service Setup** | Services: API, Kafka, Zookeeper, Postgres, Redis, Dashboard | `completed` `infrastructure` |
| 15 | **Environment Config System** | `.env.example`, Pydantic settings management | `completed` `backend` |
| 16 | **Basic Auth** | JWT-based login/register with token refresh | `completed` `backend` `security` |

---

## 🔄 Currently In Progress

*Active work — check the linked issue before starting something nearby.*

| # | Module | Description | Assignee | Labels |
|---|--------|-------------|----------|--------|
| 17 | **5-Class Sentiment** | Upgrading 3-class model to very negative / negative / neutral / positive / very positive | *open* | `in-progress` `ml` `nlp` |
| 18 | **Emotion Detection** | Plutchik 8-emotion classifier (joy, fear, anger, trust, etc.) using fine-tuned RoBERTa | *open* | `in-progress` `ml` `nlp` |
| 19 | **Competitor Config Panel** | UI to add/remove competitor brands for parallel monitoring | *open* | `in-progress` `frontend` |
| 20 | **Elasticsearch Integration** | Full-text search index for mentions, keyword queries | *open* | `in-progress` `database` `backend` |
| 21 | **Alert System — Email** | Threshold-based alerts dispatched via SMTP when sentiment drops | *open* | `in-progress` `backend` `alerts` |
| 22 | **WebSocket Live Feed** | Push live mention stream to dashboard without polling | *open* | `in-progress` `backend` `frontend` |

---

## 🔥 High Priority — Help Wanted

*These tasks are critical for the next milestone and need contributors now.*

| # | Task | Difficulty | Skills Needed | Labels |
|---|------|-----------|---------------|--------|
| 23 | **Aspect-level Sentiment** | Annotate and fine-tune model for per-attribute sentiment (price / quality / service / UX) | ⭐⭐⭐⭐ | PyTorch, HuggingFace, NLP | `help-wanted` `ml` `high-priority` |
| 24 | **BERTopic Integration** | Auto-discover topic clusters from mentions; surface top-5 themes per time window | ⭐⭐⭐ | BERTopic, scikit-learn | `help-wanted` `ml` `high-priority` |
| 25 | **Competitor Sentiment Dashboard** | Side-by-side sentiment and share-of-voice charts for brand vs. competitors | ⭐⭐⭐ | React, D3.js, REST API | `help-wanted` `frontend` `high-priority` |
| 26 | **Trend Forecasting — Prophet** | Time-series pipeline using Facebook Prophet to project mention volume and sentiment 7/14 days forward | ⭐⭐⭐⭐ | Prophet, pandas, time-series | `help-wanted` `ml` `high-priority` |
| 27 | **Alert System — Slack Webhook** | Extend alert module to push crisis notifications to a configured Slack channel | ⭐⭐ | Python, Slack SDK | `help-wanted` `backend` `high-priority` |
| 28 | **Bot & Spam Filter** | Rule-based + ML filter to discard bot-generated or spammy mentions before they enter the pipeline | ⭐⭐⭐ | scikit-learn, feature engineering | `help-wanted` `ml` `data-quality` `high-priority` |

---

## 🟢 Good First Issues

*Perfect for first-time contributors. Well-scoped, low risk, with clear acceptance criteria.*

| # | Task | Difficulty | Description | Labels |
|---|------|-----------|-------------|--------|
| 29 | **Add LinkedIn Scraper** | ⭐ | Extend ingestion layer with a LinkedIn mentions collector using the official API or scraping fallback | `good-first-issue` `ingestion` |
| 30 | **Source Badge in Dashboard** | ⭐ | Show a platform icon (Twitter bird, Reddit alien, etc.) next to each mention card | `good-first-issue` `frontend` |
| 31 | **Dark Mode Toggle** | ⭐ | Add light/dark theme switch to the dashboard using Tailwind's dark mode class | `good-first-issue` `frontend` `ui` |
| 32 | **Unit Tests — NLP Preprocessor** | ⭐ | Write pytest unit tests covering edge cases in the text cleaning and normalization module | `good-first-issue` `testing` `nlp` |
| 33 | **API Rate Limit Headers** | ⭐ | Return `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers on all API responses | `good-first-issue` `backend` |
| 34 | **Docker Health Checks** | ⭐ | Add `healthcheck` blocks to all services in `docker-compose.yml` | `good-first-issue` `infrastructure` |
| 35 | **Mention Volume Heatmap** | ⭐⭐ | Calendar heatmap showing daily mention volume (like the GitHub contribution graph) | `good-first-issue` `frontend` `visualization` |
| 36 | **README Badges Update** | ⭐ | Add build status, coverage, and last-commit badges to README | `good-first-issue` `documentation` |
| 37 | **Keyword Config via UI** | ⭐⭐ | Simple settings panel to add/remove tracked keywords without editing `.env` | `good-first-issue` `frontend` `backend` |

---

## 🤖 AI & ML Tasks

*For contributors with a machine learning or NLP background.*

| # | Task | Difficulty | Description | Labels |
|---|------|-----------|-------------|--------|
| 38 | **Named Entity Recognition** | ⭐⭐⭐ | Extract brands, people, products, and locations from mentions using spaCy NER | `ml` `nlp` `enhancement` |
| 39 | **Sarcasm Detection** | ⭐⭐⭐⭐ | Fine-tune a classifier to catch ironic or sarcastic mentions that fool standard sentiment models | `ml` `nlp` `research` |
| 40 | **Multilingual Sentiment** | ⭐⭐⭐ | Extend the sentiment pipeline to natively handle non-English mentions (mBERT / XLM-R) | `ml` `nlp` `enhancement` |
| 41 | **Graph Neural Network** | ⭐⭐⭐⭐⭐ | Build a GNN on the user-mention-topic graph to propagate influence scores and detect community clusters | `ml` `graph-ai` `research` |
| 42 | **Viral Prediction Score** | ⭐⭐⭐⭐ | Classify newly ingested content for viral potential based on early engagement velocity features | `ml` `forecasting` `research` |
| 43 | **Keyword Extraction** | ⭐⭐ | Unsupervised keyword/keyphrase extraction (KeyBERT or YAKE) from top-performing mentions | `ml` `nlp` `enhancement` |
| 44 | **Embedding Search** | ⭐⭐⭐ | Store mention embeddings in a vector DB (pgvector / Pinecone) to enable semantic similarity search | `ml` `database` `enhancement` |
| 45 | **Anomaly Detection** | ⭐⭐⭐ | Flag abnormal spikes in mention volume or sentiment shifts using statistical or ML-based detectors | `ml` `forecasting` `high-priority` |

---

## 🗺️ What's Next — Upcoming Milestones

### 🎯 Milestone 2 — Intelligence Layer *(Target: Q3 2025)*

- [ ] 5-class sentiment + emotion detection live in production
- [ ] Topic clustering (BERTopic) surfacing in dashboard
- [ ] Trend forecasting charts (7-day outlook)
- [ ] Competitor benchmarking view fully functional
- [ ] Slack + Email alert system shipped
- [ ] Bot/spam filter active in ingestion pipeline

### 🎯 Milestone 3 — Graph & Influencer Layer *(Target: Q4 2025)*

- [ ] Neo4j graph database integrated
- [ ] Influencer scoring and network visualization
- [ ] Community cluster detection
- [ ] Narrative propagation tracking
- [ ] Influencer leaderboard in dashboard

### 🎯 Milestone 4 — Enterprise Features *(Target: Q1 2026)*

- [ ] Multimodal ingestion (image OCR, audio transcription)
- [ ] Fake review & coordinated inauthentic behavior detection
- [ ] Generative AI report writer (auto-drafted insight summaries)
- [ ] Autonomous AI monitoring agents
- [ ] Role-based access control (RBAC) for enterprise teams
- [ ] White-label dashboard export (PDF / scheduled reports)

---

## 🏷️ Full Label Reference

Use these labels consistently on all issues and PRs.

### Status Labels

| Label | Color | Meaning |
|-------|-------|---------|
| `completed` | 🟩 Green | Merged and stable in `main` |
| `in-progress` | 🟦 Blue | Actively being worked on |
| `help-wanted` | 🟧 Orange | Needs a contributor to pick it up |
| `good-first-issue` | 🟨 Yellow | Ideal starting point for new contributors |
| `blocked` | 🟥 Red | Cannot proceed — waiting on a dependency |
| `under-review` | 🟪 Purple | PR open, awaiting code review |

### Domain Labels

| Label | Meaning |
|-------|---------|
| `ingestion` | Data collection, scrapers, API connectors |
| `nlp` | Text preprocessing, tokenization, embeddings |
| `ml` | Model training, evaluation, fine-tuning |
| `graph-ai` | Graph database, GNN, network analysis |
| `forecasting` | Time-series, trend prediction, anomaly detection |
| `backend` | FastAPI, Celery, REST endpoints, business logic |
| `frontend` | React dashboard, charts, UI components |
| `database` | PostgreSQL, Redis, Elasticsearch, schema |
| `infrastructure` | Docker, Kubernetes, CI/CD, monitoring |
| `security` | Auth, rate limiting, secrets management |
| `alerts` | Notification system (email, Slack, webhook) |
| `testing` | Unit tests, integration tests, load tests |
| `documentation` | README, docstrings, API docs, guides |
| `research` | Experimental — proof-of-concept or paper-driven |

### Priority Labels

| Label | Meaning |
|-------|---------|
| `high-priority` | Needed for the current milestone |
| `nice-to-have` | Valuable but not blocking |
| `future` | Planned for a later milestone |

### Type Labels

| Label | Meaning |
|-------|---------|
| `bug` | Something is broken |
| `enhancement` | Improving existing functionality |
| `new-feature` | Entirely new capability |
| `refactor` | Code quality improvement, no behavior change |
| `performance` | Speed, memory, or efficiency improvement |
| `data-quality` | Improving data accuracy or filtering |
| `ui` | Visual or UX improvement |
| `visualization` | Charts, graphs, dashboard widgets |

---

## 🧭 How to Contribute — Quick Checklist

```
1. [ ] Read CONTRIBUTING.md
2. [ ] Find a task in this file (or open an issue)
3. [ ] Comment on the issue to claim it
4. [ ] Fork the repo and create a branch:
        git checkout -b feature/your-task-name
5. [ ] Write code + tests
6. [ ] Run the test suite:
        pytest tests/
7. [ ] Open a PR with:
        - A clear description of what you changed
        - Screenshots (for frontend changes)
        - Labels from this guide
        - Reference to the issue: "Closes #XX"
8. [ ] Address review feedback
9. [ ] 🎉 Get merged!
```

---

## 💡 Ideas & Improvement Suggestions

Have an idea that isn't listed here? Open an issue with the `enhancement` or `research` label and describe:

- **What problem it solves**
- **What data or models it would use**
- **How it fits into the existing architecture**

All suggestions are reviewed within 48 hours.

---

<div align="center">

*Last updated: May 2026 · Maintained by the BrandSynapse AI core team*

**Every contribution — big or small — moves this platform forward. Thank you. 🙌**

</div>
