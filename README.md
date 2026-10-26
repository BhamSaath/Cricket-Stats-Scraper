# Cricket-Stats-Scraper and 

Query 23,000+ match records as JSONs. The system figures out what you want, pulls the right data, and returns a real answer grounded in actual match records.

---

## Overview

CricketIQ is a natural language analytics engine for cricket. You send a query. It routes that query through a structured data pipeline, computes the relevant statistics, and passes the results to Gemini to generate a clean response.

The LLM only sees numbers that came directly from the database. No hallucinated stats.

The core problem this solves is speed. Parsing 23,000 raw JSON match records per query was taking 2-3 minutes. Indexing that data into SQLite brought retrieval down to milliseconds. That change is what made a real query pipeline practical.

---

## How It Works

```
User Query
    |
    v
SQLite Database
23,000+ match records indexed
Aggregate stats computed locally
    |
    v
Aggregate Stats
    |
    v
Gemini API
Stats injected into prompt
LLM generates natural response
    |
    v
Answer
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data storage | SQLite |
| Raw data | 23,000+ JSON match records |
| LLM | Gemini API |
| Backend logic | Python |
| Performance layer | C++ (Phase 2) |
| Python/C++ bridge | PyBind11 (Phase 2) |

---

## Current Features

- Natural language query parsing via Gemini
- SQLite indexing of 23,000+ match records
- Aggregate stat computation: averages, totals, strike rates
- Sub-second structured retrieval

---

## Setup

```bash
git clone https://github.com/yourname/cricketiq
cd cricketiq
pip install -r requirements.txt

# Build SQLite database from JSON records
python build_db.py

# Run a query
python query.py "How does Kohli perform at Wankhede in T20s?"
```

SQLite build is required on first run. Takes roughly 2 minutes for the full record set.

---

## Roadmap

---

### Phase 2 — Advanced Filters

Granular stat filters on top of the existing pipeline.

**Player vs. Ground**
Career and recent batting and bowling stats filtered by specific venues.

**Player vs. Player**
Head-to-head matchup records between any batter and bowler pair, filterable by format: Test, ODI, T20.

**Phase-Based Matchups**
Any PVP or PVG query split by match phase: Powerplay, middle overs, or death overs. Economy rates, strike rates, and dismissal methods per phase.

---

### Phase 3 — Intent Resolution and Query Routing

Right now the system relies on the user knowing roughly what they want. Phase 3 adds an intent layer. The query comes in as raw text, the system classifies what kind of question it is, and routes it to the right pipeline.

```
Raw Text Input
        |
        v
AI Intent Layer
Classifies the query as PVP, PVG, or General
        |
     ---+-------------------+
     |                      |
     v                      v
PVP / PVG Query         General Question
     |                      |
     v                      v
C++ Compute Layer       AI Dialogue Layer
Fast stat calculation   Scopes the question:
via PyBind11            format, player, phase, venue
     |                      |
     |                 Struct built from user input
     |                      |
     |                      v
     |                 PyBind11 -> C++
     |                 Raw data pulled against struct
     |                      |
     +----------+-----------+
                |
                v
         AI Final Layer
         Summarizes results in natural language
```

Three query paths:

**PVP** — Raw text classified as player vs. player. C++ computes head-to-head stats. Gemini summarizes.

**PVG** — Raw text classified as player vs. ground. C++ computes venue stats. Gemini summarizes.

**General** — Raw text classified as a general question. An AI dialogue loop scopes the question, builds a struct from the user's input, passes it to C++ via PyBind11, and Gemini answers against the retrieved records.

The general path is the closest this system gets to true RAG. The model answers from retrieved raw data rather than from its weights. The retrieval is structured and C++-driven rather than vector-based, which for tabular sports data is more accurate anyway.

---

## Status

| Component | Status |
|---|---|
| JSON to SQLite pipeline | Complete |
| Gemini API integration | Complete |
| Natural language querying | Complete |
| PVP filter | In development |
| PVG filter | In development |
| Phase-based matchups | In development |
| C++ compute layer | Planned |
| PyBind11 integration | Planned |
| Intent resolution layer | Planned |
