# Cricket Analytics & AI Matchup Engine

Most cricket stats tools give you a career average and call it a day. This one answers the questions that actually matter. How does Kohli perform specifically against Bumrah? What does Rohit Sharma's record look like at Wankhede across all three formats?

Real answers. From 23,000+ real matches. No Wikipedia, no estimates.

---

## What it actually does

Two query modes, both fully working:

**Player vs. Player** — Type a batter and a bowler. Get their complete head-to-head record split by Test, ODI, and T20. Runs, balls, strike rate, average, fours, sixes, dismissal types, all of it.

**Player vs. Ground** — Type any player and any venue. Get their batting and bowling record at that ground, across every format they've played there.

The AI summary at the end only talks about numbers that came out of the database. It has no idea what Kohli's reputation is. It just sees the stats and writes about those.

---

## The problem it solves (and why it was hard)

The raw data is 23,000+ individual JSON files, one per match, ball-by-ball. The obvious approach is to loop through all of them on every query and parse what you need.

That takes 2 to 3 minutes per query. That's not a tool, that's a waiting room.

The fix was building a proper pipeline. Everything gets indexed into SQLite once. Then a C++ aggregation layer runs the actual stat computation against that database. The whole query across 23,000 matches now takes milliseconds.

The C++ piece is what makes this interesting from an engineering standpoint. It's not just glue code. It tracks match state across innings, handles format detection, computes dismissal breakdowns per format, and returns clean aggregate structs. Those structs get handed to Python via a pybind11 shared library, which passes the numbers straight into a Gemini prompt.

The LLM never touches raw data. It sees computed stats and nothing else.

---

## Architecture

```
  You type a name or venue
            │
            ▼
  ┌─────────────────────────┐
  │   Python Orchestration  │
  │   Parses input          │
  │   Routes to PVP or PVG  │
  └────────────┬────────────┘
               │  pybind11 (.so bridge)
               ▼
  ┌─────────────────────────┐
  │   C++ Aggregation Layer │
  │   PVP.cpp / PVG.cpp     │
  │   Per-delivery loop     │
  │   Format detection      │
  │   Stat computation      │
  └────────────┬────────────┘
               │  AggregateStats struct
               ▼
  ┌─────────────────────────┐
  │   SQLite Database       │
  │   23,000+ matches       │
  │   Indexed by player,    │
  │   venue, format         │
  └────────────┬────────────┘
               │
               ▼
  ┌─────────────────────────┐
  │   Gemini API            │
  │   Structured prompt     │
  │   Stats in, words out   │
  └────────────┬────────────┘
               │
               ▼
     Clean terminal output
```

---

## Tech stack

| Layer | What's running it |
|---|---|
| Raw data | Cricsheet, 23,000+ ball-by-ball JSON records |
| Database | SQLite |
| Stat engine | C++ (PVP.cpp, PVG.cpp) |
| C++/Python bridge | pybind11, statsPVP.so |
| Orchestration | Python |
| AI summary | Gemini API |

---

## Setup

```bash
git clone https://github.com/BhamSaath/Cricket-Stats-Scraper
cd Cricket-Stats-Scraper
pip install -r requirements.txt

# One-time database build, takes about 2 minutes
python3 "Python Core/build_db.py"

# Compile the C++ layer
c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) \
  -I"CPP Core" -I"include" \
  bindings.cpp "CPP Core/PVP.cpp" "CPP Core/PVG.cpp" \
  -o statsPVP.so -lsqlite3 -undefined dynamic_lookup

# Run
python3 "Python Core/main.py"
```

> macOS only: `-undefined dynamic_lookup` is a macOS linker flag. Remove it on Linux.

---

## Trying it

```
Enter 1 for Player v Player or Enter 2 for Player at Ground: 1
Batter: V Kohli
Bowler: JJ Bumrah
```

```
Enter 1 for Player v Player or Enter 2 for Player at Ground: 2
Player: JJ Bumrah
Ground: Wankhede Stadium, Mumbai
```

Names use initials and last name: `RG Sharma`, `V Kohli`, `JJ Bumrah`. Venues use the full name as stored in Cricsheet: `Wankhede Stadium, Mumbai`.

---

## What's built, what's coming

| Feature | Status |
|---|---|
| JSON to SQLite ingestion pipeline | ✅ Done |
| C++ aggregation engine | ✅ Done |
| pybind11 shared library bridge | ✅ Done |
| Player vs. Player (all 3 formats) | ✅ Done |
| Player vs. Ground (all 3 formats) | ✅ Done |
| Gemini AI summaries | ✅ Done |
| Fuzzy name matching | ✅ Done |
| Free-text intent routing | ✅ Done |
| General cricket questions | ✅ Done |
| Phase-based stats (Powerplay, middle, death overs) | 🔜 Coming |

---

## What's next

Right now you pick a mode from a menu. The plan is to cut that entirely and just let you type what you want:

> "How does Rohit Sharma bat in the death overs at Wankhede?"

An intent layer classifies the question, figures out which pipeline to run, builds the query struct, and fires it to C++. Gemini answers from whatever comes back. No vector search, no embeddings, just structured retrieval against real records.
