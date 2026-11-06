import string
import sys
import csv
sys.path.append('/Users/saathwikbhamidipaty/Cricket-Stats-Scraper')
#print("importing statsPVP")
import statsPVP
#print("imported")
import google.genai as genai
import os
api_key = os.environ.get("GEMINI_API_KEY")
def promptFilter(prompt):
    fillerWords = {
    "vs", "v", "versus", "against", "at", "in", "on", "play", "plays", 

    "played", "stats", "statistics", "record", "show", "tell", "me", "about",

    "how", "what", "who", "where", "when", "why", "do", "does", "did",
    
    "the", "a", "an", "and", "or", "but", "if", "then",
    
    "to", "for", "of", "with", "by", "from", "he", "him", "his", "they", "their",
    
    "is", "are", "was", "were", "has", "have", "had", "get", "got", "can", "could"}
    names = []
    for word in prompt.split():
        cleanWord = word.strip(string.punctuation)

        if(cleanWord and cleanWord.lower() not in fillerWords):
            names.append(cleanWord)
    return names
    
def main():
    
    print("Welcome to AI Matchup Engine for Cricket")
    prompt = input("Enter the statistic or cricket insight you want: ")
    names = promptFilter(prompt)
    namesFound = []
    batterName = "" 
    bowlerName = ""
    for name in names:
        file_path = "fuzzy_search/names.csv"
        with open(file_path, mode = "r", newline="", encoding="utf-8") as file: 
            reader = csv.reader(file)
            for row in reader: 
                if any(name.lower() in col.lower() for col in row):
                    match_str = f"[{row[0]} : {row[1]}]"
                    if match_str not in namesFound:
                        namesFound.append(match_str)
    
    #Grounds Search: 
    groundsFound = []
    for name in names:
            file_path = "fuzzy_search/venue_names.csv"
            with open(file_path, mode = "r", newline="", encoding="utf-8") as file: 
                reader = csv.reader(file)
                for row in reader: 
                    if any(name.lower() in col.lower() for col in row):
                        match_str = f"[{row[0]} : {row[1]}]"
                        if match_str not in groundsFound:
                            groundsFound.append(match_str)
    
    router_prompt = f"""You are the routing engine for a C++ cricket statistics aggregator. 
    You will receive a User Query and a list of Database Matches (format: [ID: Name]).
    
    Your strict task is to determine the user's intent and output EXACTLY ONE LINE in one of the following three formats. Do not output any conversational text, greetings, or markdown symbols.
    
    1. Player vs Player (PVP) - The user wants stats of a batter against a bowler.
    Format: PVP | batter_id | bowler_id
    Rule: The first ID must be the batter, the second the bowler. Extract the hex IDs from the Database Matches. If there are multiple players with similar names, choose the most famous international cricketers relevant to the query (e.g., choose "Rohit Sharma" over "Rohit Motwani", "Pat Cummins" over "Miguel Cummins").
    
    2. Player vs Ground (PVG) - The user wants stats of a player at a specific stadium/venue.
    Format: PVG | player_id | venue_id
    Rule: Extract the exact hex IDs from the Database Matches.
    
    3. Open Question (OQ) - The user is asking a general cricket question, rule clarification, or fact that DOES NOT require pulling match stats from the database.
    Format: OQ | [Your short, direct natural language answer]
    Rule: Provide the answer immediately after the prefix. Keep it under 4 sentences and a minimum of 2 sentences.
    
    User Query: "{prompt}"
    Database Names: {", ".join(namesFound)}
    Database Grounds: {", ".join(groundsFound)}
    """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=router_prompt) 

    modeResponse = response.text.split("|")
    
    if("PVP" in modeResponse[0]):
        batterID = modeResponse[1].strip()
        bowlerID = modeResponse[2].strip()

        with open("fuzzy_search/names.csv", mode="r", newline="", encoding="utf-8") as f:
        
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == batterID:
                    batterName = row[1]
                if row and row[0] == bowlerID:
                    bowlerName = row[1]

        pvpResult = statsPVP.queryPVP(batterID,bowlerID)
        print("\n" + "="*80)
        print(f"{'CRICKET MATCHUP STATISTICS: BATTER vs BOWLER':^80}")
        print("="*80)
        print(f"{'Format':<10} | {'Matches':<8} | {'Runs':<6} | {'Balls':<6} | {'SR':<8} | {'Avg':<8} | {'4s':<4} | {'6s':<4} | {'Wickets':<8}")
        print("-" * 80)

        formats = ["Test", "ODI", "T20"]
        for i, stats in enumerate(pvpResult):
            fmt_name = formats[i]
            print(f"{fmt_name:<10} | {stats.totalMatchesPlayed:<8} | {stats.totalRuns:<6} | {stats.totalBallsFaced:<6} | {stats.totalStrikeRate:<8.2f} | {stats.totalAverage:<8.2f} | {stats.totalFours:<4} | {stats.totalSixes:<4} | {stats.totalWickets:<8}")

        print("="*80)
        prompt = f"""You are a cricket analyst. Summarize the following head-to-head stats between batter {batterName} and bowler {bowlerName} in natural language, like a professional commentator would:


       Test Runs scored: {pvpResult[0].totalRuns}
       Test Balls faced: {pvpResult[0].totalBallsFaced}
       Test Strike rate: {pvpResult[0].totalStrikeRate:.2f}
       Test Average: {pvpResult[0].totalAverage:.2f}
       Test Fours: {pvpResult[0].totalFours}
       Test Sixes: {pvpResult[0].totalSixes}
       Test Wickets lost: {pvpResult[0].totalWickets}
       Test Bowled: {pvpResult[0].totalBowledOuts}
       Test LBW: {pvpResult[0].totalLBWs}
       Test Caught: {pvpResult[0].totalCatchOuts}
       Test Matches played: {pvpResult[0].totalMatchesPlayed}
      
       ODI Runs scored: {pvpResult[1].totalRuns}
       ODI Balls faced: {pvpResult[1].totalBallsFaced}
       ODI Strike rate: {pvpResult[1].totalStrikeRate:.2f}
       ODI Average: {pvpResult[1].totalAverage:.2f}
       ODI Fours: {pvpResult[1].totalFours}
       ODI Sixes: {pvpResult[1].totalSixes}
       ODI Wickets lost: {pvpResult[1].totalWickets}
       ODI Bowled: {pvpResult[1].totalBowledOuts}
       ODI LBW: {pvpResult[1].totalLBWs}
       ODI Caught: {pvpResult[1].totalCatchOuts}
       ODI Matches played: {pvpResult[1].totalMatchesPlayed}


       T20 Runs scored: {pvpResult[2].totalRuns}
       T20 Balls faced: {pvpResult[2].totalBallsFaced}
       T20 Strike rate: {pvpResult[2].totalStrikeRate:.2f}
       T20 Average: {pvpResult[2].totalAverage:.2f}
       T20 Fours: {pvpResult[2].totalFours}
       T20 Sixes: {pvpResult[2].totalSixes}
       T20 Wickets lost: {pvpResult[2].totalWickets}
       T20 Bowled: {pvpResult[2].totalBowledOuts}
       T20 LBW: {pvpResult[2].totalLBWs}
       T20 Caught: {pvpResult[2].totalCatchOuts}
       T20 Matches played: {pvpResult[2].totalMatchesPlayed}
      


       A format with 0 balls faced means the two have never met in it.


   Write plain text for a terminal. No markdown symbols such as ** or #. Use exactly this structure:


   MATCHUP REPORT: {batterName} vs {bowlerName}


   For each of Test, ODI and T20, in that order:
   [FORMAT NAME]
   - Edge: Batter, Bowler, or Even, with a one-line reason citing at least two numbers
   - Key numbers: runs, balls, strike rate, dismissals, fours, sixes
   - Batter strengths and weaknesses: one bullet each
   - Bowler strengths and weaknesses: one bullet each
   If a format has fewer than 30 balls, write one line saying the sample is too small to conclude anything and skip the rest of that section. If it has 0 balls, write "No data."


   OVERALL VERDICT
   - Who comes out ahead across formats and why (2-3 bullets)


   TIPS
   - For the batter: 2-3 bullets
   - For the bowler: 2-3 bullets


   Keep every bullet to one sentence."""
        client = genai.Client(api_key=api_key)
        pvpResponse = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)
        print(pvpResponse.text)

    elif("PVG" in modeResponse[0]):
         playerID = modeResponse[1].strip()
         venueID = modeResponse[2].strip()
        
        # look up venue name from register
         venueName = ""
         with open("fuzzy_search/venue_names.csv", mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == venueID:
                    venueName = row[1]  # name column
                    break
        
         if not venueName:
            print("Venue not found")
            

         pvgResult = statsPVP.queryPVG(playerID, f"%{venueName}%")
         print("\n" + "="*85)
         print(f"{'CRICKET GROUND STATISTICS: PLAYER AT VENUE':^85}")
         print("="*85)
         print(f"{'--- BATTING PERFORMANCE ---':^85}")
         print(f"{'Format':<10} | {'Matches':<8} | {'Runs':<6} | {'Balls':<6} | {'SR':<8} | {'Avg':<8} | {'4s':<4} | {'6s':<4}")
         print("-" * 85)

         batting_stats = [pvgResult.battingTest, pvgResult.battingODI, pvgResult.battingT20]
         formats = ["Test", "ODI", "T20"]
         for i, stats in enumerate(batting_stats):
            print(f"{formats[i]:<10} | {stats.totalMatchesPlayed:<8} | {stats.totalRuns:<6} | {stats.totalBallsFaced:<6} | {stats.totalStrikeRate:<8.2f} | {stats.totalAverage:<8.2f} | {stats.totalFours:<4} | {stats.totalSixes:<4}")

         print("-" * 85)
         print(f"{'--- BOWLING PERFORMANCE ---':^85}")
         print(f"{'Format':<10} | {'Matches':<8} | {'Overs':<6} | {'Runs':<6} | {'Wkts':<6} | {'Econ':<8}")
         print("-" * 85)

         bowling_stats = [pvgResult.bowlingTest, pvgResult.bowlingODI, pvgResult.bowlingT20]
         for i, stats in enumerate(bowling_stats):
             print(f"{formats[i]:<10} | {stats.totalMatchesPlayed:<8} | {stats.totalOversBowled:<6} | {stats.totalRunsConceded:<6} | {stats.totalWickets:<6} | {stats.economy:<8.2f}")

         print("="*85)
         pvg_prompt = f"""You are a cricket analyst. Summarize the following stats for {playerID} at {venueName} in natural language, like a professional commentator would.

         Write plain text for a terminal. No markdown symbols such as ** or #. Use exactly this structure:

         GROUND REPORT: {playerID} at {venueName}

         BATTING
         - Test: {pvgResult.battingTest.totalRuns} runs, {pvgResult.battingTest.totalBallsFaced} balls, SR {pvgResult.battingTest.totalStrikeRate:.2f}, Avg {pvgResult.battingTest.totalAverage:.2f}, {pvgResult.battingTest.totalFours} fours, {pvgResult.battingTest.totalSixes} sixes, {pvgResult.battingTest.totalDismissals} dismissals across {pvgResult.battingTest.totalMatchesPlayed} matches
         - ODI: {pvgResult.battingODI.totalRuns} runs, {pvgResult.battingODI.totalBallsFaced} balls, SR {pvgResult.battingODI.totalStrikeRate:.2f}, Avg {pvgResult.battingODI.totalAverage:.2f}, {pvgResult.battingODI.totalFours} fours, {pvgResult.battingODI.totalSixes} sixes, {pvgResult.battingODI.totalDismissals} dismissals across {pvgResult.battingODI.totalMatchesPlayed} matches
         - T20: {pvgResult.battingT20.totalRuns} runs, {pvgResult.battingT20.totalBallsFaced} balls, SR {pvgResult.battingT20.totalStrikeRate:.2f}, Avg {pvgResult.battingT20.totalAverage:.2f}, {pvgResult.battingT20.totalFours} fours, {pvgResult.battingT20.totalSixes} sixes, {pvgResult.battingT20.totalDismissals} dismissals across {pvgResult.battingT20.totalMatchesPlayed} matches

         BOWLING
         - Test: {pvgResult.bowlingTest.totalWickets} wickets, {pvgResult.bowlingTest.totalOversBowled} overs, {pvgResult.bowlingTest.totalRunsConceded} runs conceded, economy {pvgResult.bowlingTest.economy:.2f} across {pvgResult.bowlingTest.totalMatchesPlayed} matches
         - ODI: {pvgResult.bowlingODI.totalWickets} wickets, {pvgResult.bowlingODI.totalOversBowled} overs, {pvgResult.bowlingODI.totalRunsConceded} runs conceded, economy {pvgResult.bowlingODI.economy:.2f} across {pvgResult.bowlingODI.totalMatchesPlayed} matches
         - T20: {pvgResult.bowlingT20.totalWickets} wickets, {pvgResult.bowlingT20.totalOversBowled} overs, {pvgResult.bowlingT20.totalRunsConceded} runs conceded, economy {pvgResult.bowlingT20.economy:.2f} across {pvgResult.bowlingT20.totalMatchesPlayed} matches

         If a format has 0 balls faced and 0 balls bowled, write "No data."

         VERDICT
         - 2-3 bullets summarizing how this player performs at this ground overall

         Keep every bullet to one sentence."""

         pvgResponse = client.models.generate_content(model="gemini-3.1-flash-lite", contents=pvg_prompt)
         print(pvgResponse.text)
    elif "OQ" in modeResponse[0]:
        print(f"\nAI Answer: {modeResponse[1].strip()}")
         
if __name__ == "__main__":
           main()  
