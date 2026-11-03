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
#include <sqlite3.h>
namespace PVG
{

    struct BatterAggregate 
    {
        int totalRuns = 0;
        int totalBallsFaced = 0;
        int totalFours = 0;
        int totalSixes = 0;
        int totalMatchesPlayed = 0;
        int totalDismissals = 0;
        int totalCatchOuts = 0;
        int totalLBWs = 0;
        int totalBowledOuts = 0;
        double totalAverage = 0;
        double totalStrikeRate = 0;
    };

    struct BowlerAggregate 
    {
        int totalRunsConceded = 0;
        int totalBallsBowled = 0;
        int totalOversBowled = 0;
        int totalWickets = 0;
        int totalCatchOuts = 0;
        int totalLBWs = 0;
        int totalBowledOuts = 0;
        int totalMatchesPlayed = 0;
        int extraRuns = 0;
        double economy = 0;
    };

    struct PVGResult {
        BatterAggregate battingTest, battingODI, battingT20;
        BowlerAggregate bowlingTest, bowlingODI, bowlingT20;
    };

    std::vector <PVGResult> queryPVG(std::string namePlayer1, std::string groundName);
}