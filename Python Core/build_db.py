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
        batter TEXT,
        bowler TEXT,
        runs_batter INTEGER,
        extras INTEGER,
        wicket_kind TEXT
    )""")
for filename in os.listdir("all_json"):
    if filename.endswith(".json"):
        match_id = filename.replace(".json", "")
        with open(os.path.join("all_json", filename), "r") as f:
            with open(os.path.join("all_json", filename), "r") as f:
                try:
                    match = json.load(f)
                except json.JSONDecodeError:
                    continue
            for inning in match["innings"]:
                if "overs" not in inning:
                    continue
                for over in inning["overs"]:
                    for delivery in over["deliveries"]:
                        batter = delivery["batter"]
                        bowler = delivery["bowler"]
                        runs = int(delivery["runs"]["batter"])
                        extras = int(delivery["runs"]["extras"])
                        wicketKind = delivery["wickets"][0]["kind"] if "wickets" in delivery else None

                        cursor.execute("INSERT INTO deliveries VALUES (?, ?, ?, ?, ?, ?)", (match_id, batter, bowler, runs, extras, wicketKind))
conn.commit()
        