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
    batterName = input("Enter the Batter's name (Format: (First Initial)(Middle Initial *Optional*)(Last Name) => RG Sharma or V Kohli): ")
    bowlerName = input("Enter the Bowler's name (Format: (First Initial)(Middle Initial *Optional*)(Last Name) => JJ Bumrah or B Kumar): " )
    queryResult = statsPVP.query(batterName,bowlerName)
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
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    print(response.text)
if __name__ == "__main__":
    main()
