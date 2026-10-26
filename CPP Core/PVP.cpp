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


namespace PVP {
    
    AggregateStats query(std::string namePlayer1, std::string namePlayer2)
    {
        std::cout << "SQLite path" << std::endl;
        AggregateStats player1v2Stats;
        sqlite3* db;
        sqlite3_open("allCricketMatches.db", &db);
        sqlite3_stmt* stmt;
        sqlite3_prepare_v2(db, "SELECT match_id, runs_batter, extras, wicket_kind FROM deliveries WHERE batter = ? AND bowler = ?", -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, namePlayer1.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, namePlayer2.c_str(), -1, SQLITE_STATIC);
        std::string lastMatchId = "";
        while (sqlite3_step(stmt) == SQLITE_ROW) 
        {
            std::string currentMatchId = (const char*)sqlite3_column_text(stmt, 0);
            if(currentMatchId != lastMatchId) 
            {
                player1v2Stats.totalMatchesPlayed++;
                lastMatchId = currentMatchId;
            }
            int runsForBall = sqlite3_column_int(stmt,1);
            if(runsForBall == 4)
                player1v2Stats.totalFours++;
            if(runsForBall == 6)
                player1v2Stats.totalSixes++;
            player1v2Stats.totalBallsFaced++;
            player1v2Stats.totalRuns += runsForBall;
            player1v2Stats.extraRuns += sqlite3_column_int(stmt,2);
            const char* wicketKind = (const char*)sqlite3_column_text(stmt,3);
            if( NULL != wicketKind)
            {
                player1v2Stats.totalWickets++;
                if(strcmp(wicketKind, "bowled") == 0)
                    player1v2Stats.totalBowledOuts +=1;
                else if(strcmp(wicketKind, "lbw") == 0)
                    player1v2Stats.totalLBWs +=1;
                else if(strcmp(wicketKind, "caught")==0)
                    player1v2Stats.totalCatchOuts +=1;
            }

        }
        if(player1v2Stats.totalBallsFaced%6 != 0)
            player1v2Stats.economy = ((double)player1v2Stats.totalRuns)/((double)player1v2Stats.totalBallsFaced/6.0);
        if(player1v2Stats.totalMatchesPlayed != 0)
            player1v2Stats.totalAverage = (double)player1v2Stats.totalRuns/(double)player1v2Stats.totalMatchesPlayed;
        if(player1v2Stats.totalBallsFaced != 0)
            player1v2Stats.totalStrikeRate = ((double)player1v2Stats.totalRuns/(double)player1v2Stats.totalBallsFaced)*100;

        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return player1v2Stats;
    }
}
