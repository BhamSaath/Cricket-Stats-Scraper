import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
import json
conn = sqlite3.connect("allCricketMatches.db")
print("DB connected")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        match_id TEXT,
        matchYear INTEGER,
        matchType TEXT,
        matchVenue TEXT,
        batter TEXT,
        bowler TEXT,
        runs_batter INTEGER,
        extras INTEGER,
        wicket_kind TEXT,
        batter_ID TEXT,
        bowler_ID TEXT

    )""")
for filename in os.listdir("all_json"):
    if filename.endswith(".json"):
        match_id = filename.replace(".json", "")
        with open(os.path.join("all_json", filename), "r") as f:
            try:
                match = json.load(f)
            except json.JSONDecodeError:
                continue
        
        info = match.get("info", {})
        matchType = info.get("match_type", "UNKNOWN")
        dates = info.get("dates", [])
        matchYear = dates[0][0:4] if dates else 0
        matchVenue = info.get("venue", "UNKNOWN")
        people_registry = info.get("registry", {}).get("people", {})
        for inning in match.get("innings",[]):

            if "overs" not in inning:
                continue
            for over in inning["overs"]:
                for delivery in over["deliveries"]:
                    batter = delivery["batter"]
                    bowler = delivery["bowler"]
                    runs = int(delivery["runs"]["batter"])
                    extras = int(delivery["runs"]["extras"])
                    wicketKind = delivery["wickets"][0]["kind"] if "wickets" in delivery else None
                    batter_ID = people_registry.get(batter,"UNKNOWN")
                    bowler_ID = people_registry.get(bowler,"UNKNOWN")
                    cursor.execute("INSERT INTO deliveries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (match_id, matchYear, matchType, matchVenue,batter, bowler, runs, extras, wicketKind, batter_ID, bowler_ID))
conn.commit()
        