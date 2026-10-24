#include <string>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <random>
#include <array>
#include "PVP.h"
#include "nlohmann/json.hpp"
#include <filesystem>


namespace PVP {
    
    AggregateStats query(std::string namePlayer1, std::string namePlayer2)
    {
        AggregateStats player1v2Stats;
        
        for(const auto& entry : std:: filesystem::directory_iterator("all_json") )
        {
            if(entry.path().extension() == ".json")
            {
                std::ifstream file(entry.path());
                nlohmann::json match = nlohmann::json::parse(file);
                bool matchCounted = false;
                for(auto& inning : match["innings"])
                {
                    
                    for(auto& overs: inning["overs"])
                    {
                        for(auto& delivery: overs["deliveries"])
                        {
                            
                            if(delivery["batter"] == namePlayer1 && delivery["bowler"] == namePlayer2)
                            {
                                if(!matchCounted)
                                {
                                    matchCounted = true;
                                    player1v2Stats.totalMatchesPlayed++;
                                }
                            
                                player1v2Stats.totalRuns += delivery["runs"]["batter"].get<int>();
                                player1v2Stats.totalBallsFaced++;
                                if(delivery["runs"]["batter"].get<int>() == 4)
                                {
                                    player1v2Stats.totalFours++;
                                }
                                else if(delivery["runs"]["batter"].get<int>() == 6)
                                {
                                    player1v2Stats.totalSixes++;
                                }

                                if(delivery.contains("wickets"))
                                {
                                    if(delivery["wickets"][0]["kind"] == "bowled")
                                    {
                                        player1v2Stats.totalBowledOuts++;
                                    }
                                    else if(delivery["wickets"][0]["kind"] == "lbw")
                                    {
                                        player1v2Stats.totalLBWs++;
                                    }
                                    else if(delivery["wickets"][0]["kind"] == "caught")
                                    {
                                        player1v2Stats.totalCatchOuts++;
                                    }
                                }
                                
                            }
                        }
                    }
                }
                
            }
            
        }
        player1v2Stats.totalAverage = (double)(player1v2Stats.totalRuns) / (double)(player1v2Stats.totalMatchesPlayed);
        player1v2Stats.totalStrikeRate = (double)(player1v2Stats.totalRuns) / (double)(player1v2Stats.totalBallsFaced) * 100;
        player1v2Stats.totalOversBowled = player1v2Stats.totalBallsFaced / 6;
        player1v2Stats.totalWickets = player1v2Stats.totalBowledOuts + player1v2Stats.totalLBWs + player1v2Stats.totalCatchOuts;
        return player1v2Stats;
    }
}
