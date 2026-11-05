import sys
sys.path.append('/Users/saathwikbhamidipaty/Cricket-Stats-Scraper')
#print("importing statsPVP")
import statsPVP
#print("imported")
import google.genai as genai
import os
api_key = os.environ.get("GEMINI_API_KEY")
def main():
    
    print("Welcome to AI Matchup Engine for Cricket")
    methodCheck = input("Enter 1 for Player v Player Statistics or Enter 2 for Player at Ground Statistics: ")
    if(methodCheck == "1"):
    
        batterName = input("Enter the Batter's name (Format: (First Initial)(Middle Initial *Optional*)(Last Name) => RG Sharma or V Kohli): ")
        bowlerName = input("Enter the Bowler's name (Format: (First Initial)(Middle Initial *Optional*)(Last Name) => JJ Bumrah or B Kumar): " )
        queryResult = statsPVP.queryPVP(batterName,bowlerName)
        #Test Stats:
        print("Test Stats:\n")
        print("Total Test Wickets: "+str(queryResult[0].totalWickets))
        print("Total Test Overs: "+str(queryResult[0].totalOversBowled))
        print("Total Test Catch Outs: "+str(queryResult[0].totalCatchOuts))
        print("Total Test LBWs: "+str(queryResult[0].totalLBWs))
        print("Total Test Bowled Outs: "+str(queryResult[0].totalBowledOuts))
        print("Total Test Fours: "+str(queryResult[0].totalFours))
        print("Total Test Sixes: " +str(queryResult[0].totalSixes))
        print(f"Total Test Batter Average: {queryResult[0].totalAverage:.2f}")
        print(f"Total Test Strike Rate: {queryResult[0].totalStrikeRate:.2f}")
        print("Total Test Runs: "+str(queryResult[0].totalRuns))
        print("Total Test Balls Faced: "+str(queryResult[0].totalBallsFaced))
        print("Total Test Matches Played: "+str(queryResult[0].totalMatchesPlayed)+"\n")

        #ODI Stats: 
        print("ODI Stats:\n")
        print("Total ODI Wickets: "+str(queryResult[1].totalWickets))
        print("Total ODI Overs: "+str(queryResult[1].totalOversBowled))
        print("Total ODI Catch Outs: "+str(queryResult[1].totalCatchOuts))
        print("Total ODI LBWs: "+str(queryResult[1].totalLBWs))
        print("Total ODI Bowled Outs: "+str(queryResult[1].totalBowledOuts))
        print("Total ODI Fours: "+str(queryResult[1].totalFours))
        print("Total ODI Sixes: " +str(queryResult[1].totalSixes))
        print(f"Total ODI Batter Average: {queryResult[1].totalAverage:.2f}")
        print(f"Total ODI Strike Rate: {queryResult[1].totalStrikeRate:.2f}")
        print("Total ODI Runs: "+str(queryResult[1].totalRuns))
        print("Total ODI Balls Faced: "+str(queryResult[1].totalBallsFaced))
        print("Total ODI Matches Played: "+str(queryResult[1].totalMatchesPlayed)+"\n")

        #T20 Stats:
        print("T20 Stats:\n")
        print("Total T20 Wickets: "+str(queryResult[2].totalWickets))
        print("Total T20 Overs: "+str(queryResult[2].totalOversBowled))
        print("Total T20 Catch Outs: "+str(queryResult[2].totalCatchOuts))
        print("Total T20 LBWs: "+str(queryResult[2].totalLBWs))
        print("Total T20 Bowled Outs: "+str(queryResult[2].totalBowledOuts))
        print("Total T20 Fours: "+str(queryResult[2].totalFours))
        print("Total T20 Sixes: " +str(queryResult[2].totalSixes))
        print(f"Total T20 Batter Average: {queryResult[2].totalAverage:.2f}")
        print(f"Total T20 Strike Rate: {queryResult[2].totalStrikeRate:.2f}")
        print("Total T20 Runs: "+str(queryResult[2].totalRuns))
        print("Total T20 Balls Faced: "+str(queryResult[2].totalBallsFaced))
        print("Total T20 Matches Played: "+str(queryResult[2].totalMatchesPlayed)+"\n")

        prompt = f"""You are a cricket analyst. Summarize the following head-to-head stats between batter {batterName} and bowler {bowlerName} in natural language, like a professional commentator would:

        Test Runs scored: {queryResult[0].totalRuns}
        Test Balls faced: {queryResult[0].totalBallsFaced}
        Test Strike rate: {queryResult[0].totalStrikeRate:.2f}
        Test Average: {queryResult[0].totalAverage:.2f}
        Test Fours: {queryResult[0].totalFours}
        Test Sixes: {queryResult[0].totalSixes}
        Test Wickets lost: {queryResult[0].totalWickets}
        Test Bowled: {queryResult[0].totalBowledOuts}
        Test LBW: {queryResult[0].totalLBWs}
        Test Caught: {queryResult[0].totalCatchOuts}
        Test Matches played: {queryResult[0].totalMatchesPlayed}
        
        ODI Runs scored: {queryResult[1].totalRuns}
        ODI Balls faced: {queryResult[1].totalBallsFaced}
        ODI Strike rate: {queryResult[1].totalStrikeRate:.2f}
        ODI Average: {queryResult[1].totalAverage:.2f}
        ODI Fours: {queryResult[1].totalFours}
        ODI Sixes: {queryResult[1].totalSixes}
        ODI Wickets lost: {queryResult[1].totalWickets}
        ODI Bowled: {queryResult[1].totalBowledOuts}
        ODI LBW: {queryResult[1].totalLBWs}
        ODI Caught: {queryResult[1].totalCatchOuts}
        ODI Matches played: {queryResult[1].totalMatchesPlayed}

        T20 Runs scored: {queryResult[2].totalRuns}
        T20 Balls faced: {queryResult[2].totalBallsFaced}
        T20 Strike rate: {queryResult[2].totalStrikeRate:.2f}
        T20 Average: {queryResult[2].totalAverage:.2f}
        T20 Fours: {queryResult[2].totalFours}
        T20 Sixes: {queryResult[2].totalSixes}
        T20 Wickets lost: {queryResult[2].totalWickets}
        T20 Bowled: {queryResult[2].totalBowledOuts}
        T20 LBW: {queryResult[2].totalLBWs}
        T20 Caught: {queryResult[2].totalCatchOuts}
        T20 Matches played: {queryResult[2].totalMatchesPlayed}
        

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
        response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)
        print(response.text)
    

    if(methodCheck == "2"):
        col = 20  # label column width
        w = 8     # stat column width
        playerName = input("Enter the Player's name (Format: (First Initial)(Middle Initial *Optional*)(Last Name) => RG Sharma or V Kohli): ")
        groundName = input("Enter the Ground's name (Format: (Ground Name), (City Name) => Wankhede, Mumbai: ")
        queryResult = statsPVP.queryPVG(playerName, groundName)
        print(f"Batting Statistics at {groundName}\n")
        print(f"{'Match Type':<{col}} {'Test':>{w}} {'ODI':>{w}} {'T20':>{w}}")
        print(f"{'Total Matches Batted':<{col}} {queryResult.battingTest.totalMatchesPlayed:>{w}} {queryResult.battingODI.totalMatchesPlayed:>{w}} {queryResult.battingT20.totalMatchesPlayed:>{w}}")
        print(f"{'Total Runs':<{col}} {queryResult.battingTest.totalRuns:>{w}} {queryResult.battingODI.totalRuns:>{w}} {queryResult.battingT20.totalRuns:>{w}}")
        print(f"{'Total Balls Faced':<{col}} {queryResult.battingTest.totalBallsFaced:>{w}} {queryResult.battingODI.totalBallsFaced:>{w}} {queryResult.battingT20.totalBallsFaced:>{w}}")
        print(f"{'Strike Rate':<{col}} {queryResult.battingTest.totalStrikeRate:>{w}.2f} {queryResult.battingODI.totalStrikeRate:>{w}.2f} {queryResult.battingT20.totalStrikeRate:>{w}.2f}")
        print(f"{'Total Average':<{col}} {queryResult.battingTest.totalAverage:>{w}.2f} {queryResult.battingODI.totalAverage:>{w}.2f} {queryResult.battingT20.totalAverage:>{w}.2f}")
        print(f"{'Total Fours':<{col}} {queryResult.battingTest.totalFours:>{w}} {queryResult.battingODI.totalFours:>{w}} {queryResult.battingT20.totalFours:>{w}}")
        print(f"{'Total Sixes':<{col}} {queryResult.battingTest.totalSixes:>{w}} {queryResult.battingODI.totalSixes:>{w}} {queryResult.battingT20.totalSixes:>{w}}")
        print(f"{'Total Dismissals':<{col}} {queryResult.battingTest.totalDismissals:>{w}} {queryResult.battingODI.totalDismissals:>{w}} {queryResult.battingT20.totalDismissals:>{w}}")
        print(f"{'Total Catch Outs':<{col}} {queryResult.battingTest.totalCatchOuts:>{w}} {queryResult.battingODI.totalCatchOuts:>{w}} {queryResult.battingT20.totalCatchOuts:>{w}}")
        print(f"{'Total LBWs':<{col}} {queryResult.battingTest.totalLBWs:>{w}} {queryResult.battingODI.totalLBWs:>{w}} {queryResult.battingT20.totalLBWs:>{w}}")
        print(f"{'Total Bowled Outs':<{col}} {queryResult.battingTest.totalBowledOuts:>{w}} {queryResult.battingODI.totalBowledOuts:>{w}} {queryResult.battingT20.totalBowledOuts:>{w}}")

        print(f"\nBowling Statistics at {groundName}\n")
        print(f"{'Match Type':<{col}} {'Test':>{w}} {'ODI':>{w}} {'T20':>{w}}")
        print(f"{'Total Matches Bowled':<{col}} {queryResult.bowlingTest.totalMatchesPlayed:>{w}} {queryResult.bowlingODI.totalMatchesPlayed:>{w}} {queryResult.bowlingT20.totalMatchesPlayed:>{w}}")
        print(f"{'Total Runs Conceded':<{col}} {queryResult.bowlingTest.totalRunsConceded:>{w}} {queryResult.bowlingODI.totalRunsConceded:>{w}} {queryResult.bowlingT20.totalRunsConceded:>{w}}")
        print(f"{'Total Balls Bowled':<{col}} {queryResult.bowlingTest.totalBallsBowled:>{w}} {queryResult.bowlingODI.totalBallsBowled:>{w}} {queryResult.bowlingT20.totalBallsBowled:>{w}}")
        print(f"{'Total Overs Bowled':<{col}} {queryResult.bowlingTest.totalOversBowled:>{w}} {queryResult.bowlingODI.totalOversBowled:>{w}} {queryResult.bowlingT20.totalOversBowled:>{w}}")
        print(f"{'Total Economy':<{col}} {queryResult.bowlingTest.economy:>{w}.2f} {queryResult.bowlingODI.economy:>{w}.2f} {queryResult.bowlingT20.economy:>{w}.2f}")
        print(f"{'Total Wickets':<{col}} {queryResult.bowlingTest.totalWickets:>{w}} {queryResult.bowlingODI.totalWickets:>{w}} {queryResult.bowlingT20.totalWickets:>{w}}")
        print(f"{'Total Catch Outs':<{col}} {queryResult.bowlingTest.totalCatchOuts:>{w}} {queryResult.bowlingODI.totalCatchOuts:>{w}} {queryResult.bowlingT20.totalCatchOuts:>{w}}")
        print(f"{'Total LBWs':<{col}} {queryResult.bowlingTest.totalLBWs:>{w}} {queryResult.bowlingODI.totalLBWs:>{w}} {queryResult.bowlingT20.totalLBWs:>{w}}")
        print(f"{'Total Bowled Outs':<{col}} {queryResult.bowlingTest.totalBowledOuts:>{w}} {queryResult.bowlingODI.totalBowledOuts:>{w}} {queryResult.bowlingT20.totalBowledOuts:>{w}}")
        print(f"{'Total Extras Given':<{col}} {queryResult.bowlingTest.extraRuns:>{w}} {queryResult.bowlingODI.extraRuns:>{w}} {queryResult.bowlingT20.extraRuns:>{w}}")

        prompt = prompt = f"""You are a cricket analyst. Summarize the following performance statistics for {playerName} at {groundName} in natural language, like a professional commentator would:

    Test Batting:
    Matches: {queryResult.battingTest.totalMatchesPlayed}
    Runs: {queryResult.battingTest.totalRuns} | Balls faced: {queryResult.battingTest.totalBallsFaced}
    Strike rate: {queryResult.battingTest.totalStrikeRate:.2f} | Average: {queryResult.battingTest.totalAverage:.2f}
    Boundaries: {queryResult.battingTest.totalFours} Fours, {queryResult.battingTest.totalSixes} Sixes
    Dismissals: {queryResult.battingTest.totalDismissals} (Caught: {queryResult.battingTest.totalCatchOuts}, LBW: {queryResult.battingTest.totalLBWs}, Bowled: {queryResult.battingTest.totalBowledOuts})
    
    Test Bowling:
    Matches: {queryResult.bowlingTest.totalMatchesPlayed}
    Overs: {queryResult.bowlingTest.totalOversBowled} | Balls: {queryResult.bowlingTest.totalBallsBowled}
    Wickets: {queryResult.bowlingTest.totalWickets} | Economy: {queryResult.bowlingTest.economy:.2f}
    Runs conceded: {queryResult.bowlingTest.totalRunsConceded} | Extras given: {queryResult.bowlingTest.extraRuns}
    Wicket types: Caught: {queryResult.bowlingTest.totalCatchOuts}, LBW: {queryResult.bowlingTest.totalLBWs}, Bowled: {queryResult.bowlingTest.totalBowledOuts}

    ODI Batting:
    Matches: {queryResult.battingODI.totalMatchesPlayed}
    Runs: {queryResult.battingODI.totalRuns} | Balls faced: {queryResult.battingODI.totalBallsFaced}
    Strike rate: {queryResult.battingODI.totalStrikeRate:.2f} | Average: {queryResult.battingODI.totalAverage:.2f}
    Boundaries: {queryResult.battingODI.totalFours} Fours, {queryResult.battingODI.totalSixes} Sixes
    Dismissals: {queryResult.battingODI.totalDismissals} (Caught: {queryResult.battingODI.totalCatchOuts}, LBW: {queryResult.battingODI.totalLBWs}, Bowled: {queryResult.battingODI.totalBowledOuts})
    
    ODI Bowling:
    Matches: {queryResult.bowlingODI.totalMatchesPlayed}
    Overs: {queryResult.bowlingODI.totalOversBowled} | Balls: {queryResult.bowlingODI.totalBallsBowled}
    Wickets: {queryResult.bowlingODI.totalWickets} | Economy: {queryResult.bowlingODI.economy:.2f}
    Runs conceded: {queryResult.bowlingODI.totalRunsConceded} | Extras given: {queryResult.bowlingODI.extraRuns}
    Wicket types: Caught: {queryResult.bowlingODI.totalCatchOuts}, LBW: {queryResult.bowlingODI.totalLBWs}, Bowled: {queryResult.bowlingODI.totalBowledOuts}

    T20 Batting:
    Matches: {queryResult.battingT20.totalMatchesPlayed}
    Runs: {queryResult.battingT20.totalRuns} | Balls faced: {queryResult.battingT20.totalBallsFaced}
    Strike rate: {queryResult.battingT20.totalStrikeRate:.2f} | Average: {queryResult.battingT20.totalAverage:.2f}
    Boundaries: {queryResult.battingT20.totalFours} Fours, {queryResult.battingT20.totalSixes} Sixes
    Dismissals: {queryResult.battingT20.totalDismissals} (Caught: {queryResult.battingT20.totalCatchOuts}, LBW: {queryResult.battingT20.totalLBWs}, Bowled: {queryResult.battingT20.totalBowledOuts})
    
    T20 Bowling:
    Matches: {queryResult.bowlingT20.totalMatchesPlayed}
    Overs: {queryResult.bowlingT20.totalOversBowled} | Balls: {queryResult.bowlingT20.totalBallsBowled}
    Wickets: {queryResult.bowlingT20.totalWickets} | Economy: {queryResult.bowlingT20.economy:.2f}
    Runs conceded: {queryResult.bowlingT20.totalRunsConceded} | Extras given: {queryResult.bowlingT20.extraRuns}
    Wicket types: Caught: {queryResult.bowlingT20.totalCatchOuts}, LBW: {queryResult.bowlingT20.totalLBWs}, Bowled: {queryResult.bowlingT20.totalBowledOuts}

    A format with 0 matches played means the player has never played at this ground in that format.

    Write plain text for a terminal. No markdown symbols such as ** or #. Use exactly this structure:

    VENUE REPORT: {playerName} at {groundName}

    For each of Test, ODI and T20, in that order:
    [FORMAT NAME]
- Ground Affinity: Excellent, Good, Average, or Poor, with a one-line reason citing at least two key numbers across bat/ball.
- Key numbers: Standout stats from batting, bowling, or both.
- Batting summary: One bullet summarizing scoring pace, average, and dismissal vulnerabilities here (skip if 0 runs).
- Bowling summary: One bullet summarizing economy, wicket-taking ability, and dismissal types (skip if 0 overs bowled).
    If a format has fewer than 2 matches played, write one line saying the sample size is too small to draw firm conclusions and skip the rest of that section. If it has 0 matches, write "No data."

    OVERALL VERDICT
- Does this player typically thrive or struggle at this venue across formats? (2-3 bullets explaining why based on the data)

    VENUE TIPS
- Batting adjustments: 1-2 bullets based on how they usually get out or score here.
- Bowling adjustments: 1-2 bullets based on their economy and most successful wicket types here.

    Keep every bullet to one sentence."""
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)    
        print(response.text)
if __name__ == "__main__":
            main()   



        


