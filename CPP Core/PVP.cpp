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
    
    std::vector <AggregateStats> query(std::string namePlayer1, std::string namePlayer2)
    {
        
        AggregateStats player1v2StatsTest;
        AggregateStats player1v2StatsODI;
        AggregateStats player1v2StatsT20;
        sqlite3* db;
        sqlite3_open("allCricketMatches.db", &db);
        sqlite3_stmt* stmt;
        sqlite3_prepare_v2(db, "SELECT match_id, matchYear, matchType, matchVenue,runs_batter, extras, wicket_kind FROM deliveries WHERE batter = ? AND bowler = ?", -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, namePlayer1.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, namePlayer2.c_str(), -1, SQLITE_STATIC);
        std::string lastMatchId = "";
        bool test = false;
        bool odi = false;
        bool t20 = false;
        while (sqlite3_step(stmt) == SQLITE_ROW) 
        {
            
            std::string currentMatchId = (const char*)sqlite3_column_text(stmt, 0);
            
            if(currentMatchId != lastMatchId) 
            {
                test = false;
                odi = false;
                t20 = false;
                const char* matchType = (const char*)sqlite3_column_text(stmt,2);
                if(strcmp(matchType, "ODM") == 0 || strcmp(matchType, "ODI") == 0)
                {
                    player1v2StatsODI.totalMatchesPlayed++;
                    odi = true;
                }
                if(strcmp(matchType, "IT20") == 0 || strcmp(matchType, "T20") == 0)
                {
                    player1v2StatsT20.totalMatchesPlayed++;
                    t20 = true;
                }
                if(strcmp(matchType, "Test") == 0 || strcmp(matchType, "MDM") == 0)
                {
                    player1v2StatsTest.totalMatchesPlayed++;
                    test = true;
                }
                lastMatchId = currentMatchId;
            }
            int runsForBall = sqlite3_column_int(stmt,4);
            //4s
            if(runsForBall == 4 && t20)
                player1v2StatsT20.totalFours++;
            else if(runsForBall == 4 && odi)
                player1v2StatsODI.totalFours++;
            else if(runsForBall == 4 && test)
                player1v2StatsTest.totalFours++;
            //6s
            if(runsForBall == 6 && t20)
                player1v2StatsT20.totalSixes++;
            else if(runsForBall == 6 && odi)
                player1v2StatsODI.totalSixes++;
            else if(runsForBall == 6 && test)
                player1v2StatsTest.totalSixes++;
            //Balls
            if(t20)
            {
                player1v2StatsT20.totalBallsFaced++;
                player1v2StatsT20.totalRuns+= runsForBall;

            }
            else if(odi)
            {
                player1v2StatsODI.totalBallsFaced++;
                player1v2StatsODI.totalRuns+= runsForBall;
            }
            else if(test)
            {
                player1v2StatsTest.totalBallsFaced++;
                player1v2StatsTest.totalRuns+= runsForBall;
            }
            if(t20)
                player1v2StatsT20.extraRuns += sqlite3_column_int(stmt,5);
            if(odi)
                player1v2StatsODI.extraRuns += sqlite3_column_int(stmt,5);
            if(test)
                player1v2StatsTest.extraRuns += sqlite3_column_int(stmt,5);


            
            const char* wicketKind = (const char*)sqlite3_column_text(stmt,6);
            if( NULL != wicketKind && odi)
            {
                player1v2StatsODI.totalWickets++;
                if(strcmp(wicketKind, "bowled") == 0)
                    player1v2StatsODI.totalBowledOuts +=1;
                else if(strcmp(wicketKind, "lbw") == 0)
                    player1v2StatsODI.totalLBWs +=1;
                else if(strcmp(wicketKind, "caught")==0)
                    player1v2StatsODI.totalCatchOuts +=1;
            }
            if( NULL != wicketKind && t20)
            {
                player1v2StatsT20.totalWickets++;
                if(strcmp(wicketKind, "bowled") == 0)
                    player1v2StatsT20.totalBowledOuts +=1;
                else if(strcmp(wicketKind, "lbw") == 0)
                    player1v2StatsT20.totalLBWs +=1;
                else if(strcmp(wicketKind, "caught")==0)
                    player1v2StatsT20.totalCatchOuts +=1;
            }
            if( NULL != wicketKind && test)
            {
                player1v2StatsTest.totalWickets++;
                if(strcmp(wicketKind, "bowled") == 0)
                    player1v2StatsTest.totalBowledOuts +=1;
                else if(strcmp(wicketKind, "lbw") == 0)
                    player1v2StatsTest.totalLBWs +=1;
                else if(strcmp(wicketKind, "caught")==0)
                    player1v2StatsTest.totalCatchOuts +=1;
            }
        }
        //Overs bowled
        player1v2StatsODI.totalOversBowled = (int)player1v2StatsODI.totalBallsFaced/6;
        player1v2StatsTest.totalOversBowled = (int)player1v2StatsTest.totalBallsFaced/6;   
        player1v2StatsT20.totalOversBowled = (int)player1v2StatsT20.totalBallsFaced/6;  
        //economy
        if(player1v2StatsT20.totalBallsFaced != 0)
            player1v2StatsT20.economy = (((double)player1v2StatsT20.totalRuns)+(double)player1v2StatsT20.extraRuns)/((double)player1v2StatsT20.totalBallsFaced/6.0);
        if(player1v2StatsTest.totalBallsFaced != 0)
            player1v2StatsTest.economy = (((double)player1v2StatsTest.totalRuns)+(double)player1v2StatsTest.extraRuns)/((double)player1v2StatsTest.totalBallsFaced/6.0);
        if(player1v2StatsODI.totalBallsFaced != 0)
            player1v2StatsODI.economy = (((double)player1v2StatsODI.totalRuns)+(double)player1v2StatsODI.extraRuns)/((double)player1v2StatsODI.totalBallsFaced/6.0);
        //Average
        if(player1v2StatsODI.totalMatchesPlayed != 0)
            player1v2StatsODI.totalAverage = (double)player1v2StatsODI.totalRuns/(double)player1v2StatsODI.totalMatchesPlayed;
        if(player1v2StatsTest.totalMatchesPlayed != 0)
            player1v2StatsTest.totalAverage = (double)player1v2StatsTest.totalRuns/(double)player1v2StatsTest.totalMatchesPlayed;
        if(player1v2StatsT20.totalMatchesPlayed != 0)
            player1v2StatsT20.totalAverage = (double)player1v2StatsT20.totalRuns/(double)player1v2StatsT20.totalMatchesPlayed;
        
        

        //Strike Rate
        if(player1v2StatsT20.totalBallsFaced != 0)
            player1v2StatsT20.totalStrikeRate = ((double)player1v2StatsT20.totalRuns/(double)player1v2StatsT20.totalBallsFaced)*100;
        if(player1v2StatsTest.totalBallsFaced != 0)
            player1v2StatsTest.totalStrikeRate = ((double)player1v2StatsTest.totalRuns/(double)player1v2StatsTest.totalBallsFaced)*100;
        if(player1v2StatsODI.totalBallsFaced != 0)
            player1v2StatsODI.totalStrikeRate = ((double)player1v2StatsODI.totalRuns/(double)player1v2StatsODI.totalBallsFaced)*100;    

        sqlite3_finalize(stmt);
        sqlite3_close(db);

        std::vector<AggregateStats> result = {player1v2StatsTest,player1v2StatsODI,player1v2StatsT20};
        return result;
    }
}
