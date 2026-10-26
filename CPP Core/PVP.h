#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <fstream>
#include <array>
#include "nlohmann/json.hpp"
namespace PVP {
    struct AggregateStats {
        //Bowler Stats
        
        int economy = 0;
        int extraRuns = 0;  
        int totalWickets = 0;
        int totalOversBowled = 0;
        int totalCatchOuts = 0; 
        int totalLBWs = 0;
        int totalBowledOuts = 0;

        //Batsman Stats
        int totalFours = 0;
        int totalSixes = 0;
        double totalAverage = 0;
        double totalStrikeRate = 0;

        
        //Common Stats
        int totalRuns = 0;
        int totalBallsFaced = 0;
        int totalMatchesPlayed = 0;

    };
    AggregateStats query(std::string namePlayer1, std::string namePlayer2);

}