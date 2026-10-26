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
    print("Total Wickets: "+str(queryResult.totalWickets))
    print("Total Overs: "+str(queryResult.totalOversBowled))
    print("Total Catch Outs: "+str(queryResult.totalCatchOuts))
    print("Total LBWs: "+str(queryResult.totalLBWs))
    print("Total Bowled Outs: "+str(queryResult.totalBowledOuts))
    print("Total Fours: "+str(queryResult.totalFours))
    print("Total Sixes: " +str(queryResult.totalSixes))
    print("Total Average: "+str(queryResult.totalAverage))
    print("Total Strike Rate: "+str(queryResult.totalStrikeRate))
    print("Total Runs: "+str(queryResult.totalRuns))
    print("Total Balls Faced: "+str(queryResult.totalBallsFaced))
    print("Total Matches Playerd: "+str(queryResult.totalMatchesPlayed))
    prompt = f"""You are a cricket analyst. Summarize the following head-to-head stats between batter {batterName} and bowler {bowlerName} in natural language, like a professional commentator would:

    Runs scored: {queryResult.totalRuns}
    Balls faced: {queryResult.totalBallsFaced}
    Strike rate: {queryResult.totalStrikeRate:.2f}
    Average: {queryResult.totalAverage:.2f}
    Fours: {queryResult.totalFours}
    Sixes: {queryResult.totalSixes}
    Wickets lost: {queryResult.totalWickets}
    Bowled: {queryResult.totalBowledOuts}
    LBW: {queryResult.totalLBWs}
    Caught: {queryResult.totalCatchOuts}
    Matches played: {queryResult.totalMatchesPlayed}

    Keep it to 3-4 sentences."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
    print(response.text)
if __name__ == "__main__":
    main()
