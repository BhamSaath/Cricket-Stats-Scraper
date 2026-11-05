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
    for name in names:
        file_path = "fuzzy_search/names.csv"
        with open(file_path, mode = "r", newline="", encoding="utf-8") as file: 
            reader = csv.reader(file)
            for row in reader: 
                if any(name.lower() in col.lower() for col in row):
                    match_str = f"[{row[0]} : {row[1]}]"
                    if match_str not in namesFound:
                        namesFound.append(match_str)
    namesList = ""
    for match in namesFound:
        namesList += match+"\n"
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
    Rule: Provide the answer immediately after the prefix. Keep it under 3 sentences.
    
    User Query: "{prompt}"
    Database Matches: {", ".join(namesFound)}
    """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=router_prompt) 
    print(response.text)

    
if __name__ == "__main__":
           main()  
