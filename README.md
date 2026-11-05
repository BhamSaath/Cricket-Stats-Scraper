# Cricket Analytics & AI Matchup Engine

Ever wanted to know exactly how Virat Kohli performs against Jasprit Bumrah across every format they've ever played? This project answers that — from real match data, not Wikipedia.

It pulls from 23,000+ ball-by-ball match records, crunches the numbers in C++, and hands the stats to Gemini to write you a clean summary. No guessing, no hallucinated averages.

---

## What it does

Two things right now:

**Player vs. Player** — Pick a batter and a bowler. Get their full head-to-head record broken down by Test, ODI, and T20. Runs, strike rate, dismissal types, the works.

**Player vs. Ground** — Pick any player and any venue. See how they bat and bowl there across every format they've played at that ground.

The AI only summarizes numbers that came out of the database. It doesn't fill in gaps from its training data.

---

## How it's built

The core engineering challenge here was performance. Naively parsing 23,000 raw JSON files on every query took 2–3 minutes — completely unusable for an interactive tool. The solution was a two-part architecture: a one-time ingestion pipeline that indexes all ball-by-ball delivery data into a structured SQLite database, and a C++ aggregation layer that runs the actual stat computation against that database at query time.

The C++ layer handles the heavy lifting — iterating over deliveries, tracking match state across innings, and computing aggregates like strike rate, economy, and dismissal breakdown per format. It exposes compiled functions to Python via a pybind11 shared library (`statsPVP.so`), which keeps the Python layer clean and focused purely on orchestration. Python handles user input, invokes the right C++ function, and passes the resulting stat struct directly into a Gemini prompt. The LLM never touches raw data — it only sees the final aggregated numbers, which keeps the summaries grounded and fast.

```
  User Input (player name / venue)
            │
            ▼
  ┌─────────────────────────┐
  │   Python Orchestration  │
  │   Routes query mode     │
  │   (PVP or PVG)          │
  └────────────┬────────────┘
               │  pybind11 call
               ▼
  ┌─────────────────────────┐
  │   C++ Aggregation Layer │
  │   PVP.cpp / PVG.cpp     │
  │   Queries SQLite        │
  │   Computes per-format   │
  │   stats per delivery    │
  └────────────┬────────────┘
               │  returns AggregateStats struct
               ▼
  ┌─────────────────────────┐
  │   SQLite Database       │
  │   23,000+ matches       │
  │   indexed by player,    │
  │   venue, match type     │
  └────────────┬────────────┘
               │
               ▼
  ┌─────────────────────────┐
  │   Gemini API            │
  │   Stats injected into   │
  │   structured prompt     │
  │   Natural language out  │
  └────────────┬────────────┘
               │
               ▼
     Terminal output + summary
```

---

## Tech stack

| Layer | What's doing the work |
|---|---|
| Raw data | Cricsheet — 23,000+ JSON match records |
| Database | SQLite |
| Stat engine | C++ (PVP.cpp, PVG.cpp) |
| Python/C++ bridge | pybind11 |
| Orchestration | Python |
| AI summary | Gemini API |
| Shared library | statsPVP.so |

---

## Setup

```bash
git clone https://github.com/BhamSaath/Cricket-Stats-Scraper
cd Cricket-Stats-Scraper
pip install -r requirements.txt

# Build the database — do this once, takes about 2 minutes
python3 "Python Core/build_db.py"

# Compile the C++ layer
c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) -I"CPP Core" -I"include" bindings.cpp "CPP Core/PVP.cpp" "CPP Core/PVG.cpp" -o statsPVP.so -lsqlite3 -undefined dynamic_lookup

# Run it
python3 "Python Core/main.py"
```

---

## Trying it out

```
Enter 1 for Player v Player or Enter 2 for Player at Ground: 1
Batter: V Kohli
Bowler: JJ Bumrah
```

```
Enter 1 for Player v Player or Enter 2 for Player at Ground: 2
Player: V Kohli
Ground: Wankhede Stadium, Mumbai
```

Names go in as initials + last name: `RG Sharma`, `V Kohli`, `JJ Bumrah`.

---

## What's done, what's next

| Feature | Status |
|---|---|
| JSON → SQLite pipeline | Done |
| C++ aggregation engine | Done |
| pybind11 bridge | Done |
| Player vs. Player | Done |
| Player vs. Ground | Done |
| Gemini summaries | Done |
| Phase-based stats (Powerplay / middle / death overs) | Coming |
| Free-text query routing | Coming |

---

## What's coming

Right now you pick a mode from a menu. The next version lets you just type what you want:

> "How does Rohit Sharma bat in death overs at Wankhede?"

An intent layer classifies the question, figures out which pipeline to run, builds the query, and passes it to C++. Gemini answers from whatever comes back. No vector search — just structured retrieval against real records.
