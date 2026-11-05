#include <string>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <random>
#include <array>
#include "PVP.h"
#include "PVG.h"
#include "nlohmann/json.hpp"
#include <filesystem>
#include <sqlite3.h>

namespace PVG
{
    PVGResult queryPVG(std::string namePlayer1, std::string groundName)
    {
        PVGResult result; 
        sqlite3* db; 
        sqlite3_open("allCricketMatches.db", &db);
        sqlite3_stmt* stmt;
        sqlite3_prepare_v2(db,
    "SELECT match_id, matchType, batter, bowler, runs_batter, extras, wicket_kind "
    "FROM deliveries WHERE (batter = ? OR bowler = ?) AND matchVenue = ? "
    "ORDER BY match_id",
    -1, &stmt, nullptr);
        sqlite3_bind_text(stmt,1,namePlayer1.c_str(),-1,SQLITE_STATIC);
        sqlite3_bind_text(stmt,2,namePlayer1.c_str(),-1,SQLITE_STATIC);
        sqlite3_bind_text(stmt,3,groundName.c_str(),-1,SQLITE_STATIC);
        std::string lastMatchId = "";
        bool test = false;
        bool odi = false;
        bool t20 = false;
        //t20s
        sqlite3_stmt* countStmt;
        sqlite3_prepare_v2(db,
            "SELECT COUNT(DISTINCT match_id) FROM deliveries WHERE bowler = ? AND matchVenue = ? AND matchType IN ('T20', 'IT20')",
            -1, &countStmt, nullptr);
        sqlite3_bind_text(countStmt, 1, namePlayer1.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(countStmt, 2, groundName.c_str(), -1, SQLITE_STATIC);
        sqlite3_step(countStmt);
        result.bowlingT20.totalMatchesPlayed = sqlite3_column_int(countStmt, 0);

        sqlite3_finalize(countStmt);

        sqlite3_stmt* countStmt2;
        sqlite3_prepare_v2(db,
            "SELECT COUNT(DISTINCT match_id) FROM deliveries WHERE batter = ? AND matchVenue = ? AND matchType IN ('T20', 'IT20')",
            -1, &countStmt2, nullptr);
        sqlite3_bind_text(countStmt2, 1, namePlayer1.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(countStmt2, 2, groundName.c_str(), -1, SQLITE_STATIC);
        sqlite3_step(countStmt2);
        result.battingT20.totalMatchesPlayed = sqlite3_column_int(countStmt2, 0);

        sqlite3_finalize(countStmt2);
            
         while (sqlite3_step(stmt) == SQLITE_ROW) 
        {
            const char* batter = (const char*)sqlite3_column_text(stmt, 2);
            const char* bowler = (const char*)sqlite3_column_text(stmt, 3); 
            if(batter == nullptr || bowler == nullptr) continue;
            std::string currentMatchId = (const char*)sqlite3_column_text(stmt, 0);
            const char* matchType = (const char*)sqlite3_column_text(stmt,1);
            if( lastMatchId != currentMatchId)
            {
                test = false;
                odi = false;
                t20 = false;
                if(strcmp(matchType, "ODM") == 0 || strcmp(matchType, "ODI") == 0)
                {
                    odi = true;
                }
                if(strcmp(matchType, "IT20") == 0 || strcmp(matchType, "T20") == 0)
                {
                    t20 = true;
                    
                }
                if(strcmp(matchType, "Test") == 0 || strcmp(matchType, "MDM") == 0)
                {
                    test = true;
                }


                
                lastMatchId = currentMatchId;
            }
            if(strcmp(batter, namePlayer1.c_str()) == 0 )
            {   
                
                
                int runsOnBall = sqlite3_column_int(stmt,4);
                int extras = sqlite3_column_int(stmt,5);
                const char* wicketKind = (const char*)sqlite3_column_text(stmt, 6);


                if(odi)
                {
                    
                    result.battingODI.totalRuns += runsOnBall;
                    result.battingODI.totalBallsFaced++;
                    if(runsOnBall == 4)
                        result.battingODI.totalFours++;
                    if(runsOnBall == 6)
                        result.battingODI.totalSixes++;
                    if(wicketKind != NULL)
                    {
                        result.battingODI.totalDismissals++;
                        if(strcmp(wicketKind, "bowled")==0)
                            result.battingODI.totalBowledOuts++;
                        else if(strcmp(wicketKind, "lbw")==0)
                            result.battingODI.totalLBWs++;
                        else if(strcmp(wicketKind, "caught")==0)
                            result.battingODI.totalCatchOuts++;
                    }
                }
                if(t20)
                {
                    
                    result.battingT20.totalRuns += runsOnBall;
                    result.battingT20.totalBallsFaced++;
                    if(runsOnBall == 4)
                        result.battingT20.totalFours++;
                    if(runsOnBall == 6)
                        result.battingT20.totalSixes++;
                    if(wicketKind != NULL)
                    {
                        result.battingT20.totalDismissals++;
                        if(strcmp(wicketKind, "bowled")==0)
                            result.battingT20.totalBowledOuts++;
                        else if(strcmp(wicketKind, "lbw")==0)
                            result.battingT20.totalLBWs++;
                        else if(strcmp(wicketKind, "caught")==0)
                            result.battingT20.totalCatchOuts++;
                    }
                }
                if(test)
                {
                    result.battingTest.totalRuns += runsOnBall;
                    result.battingTest.totalBallsFaced++;
                    if(runsOnBall == 4)
                        result.battingTest.totalFours++;
                    if(runsOnBall == 6)
                        result.battingTest.totalSixes++;
                    if(wicketKind != NULL)
                    {
                        result.battingTest.totalDismissals++;
                        if(strcmp(wicketKind, "bowled")==0)
                            result.battingTest.totalBowledOuts++;
                        else if(strcmp(wicketKind, "lbw")==0)
                            result.battingTest.totalLBWs++;
                        else if(strcmp(wicketKind, "caught")==0)
                            result.battingTest.totalCatchOuts++;
                    }
                }
                
                
            }
            if(strcmp(bowler,namePlayer1.c_str()) == 0)
            {
                int runsOnBall = sqlite3_column_int(stmt,4);
                int extras = sqlite3_column_int(stmt,5);
                const char* wicketKind = (const char*)sqlite3_column_text(stmt, 6);
                
                if(odi)
                {
                    result.bowlingODI.totalRunsConceded += runsOnBall;
                    result.bowlingODI.extraRuns += extras;
                    result.bowlingODI.totalBallsBowled++;

                    if(wicketKind != NULL)
                    {
                        result.bowlingODI.totalWickets++;
                        if(strcmp(wicketKind, "bowled")==0)
                        {
                            result.bowlingODI.totalBowledOuts++;
                        }
                        else if(strcmp(wicketKind, "lbw")==0)
                        {
                            result.bowlingODI.totalLBWs++;
                        }
                        else if(strcmp(wicketKind, "caught")==0)
                        {
                            result.bowlingODI.totalCatchOuts++;
                        }
                    }


                }
                if(t20)
                {
                    result.bowlingT20.totalRunsConceded += runsOnBall;
                    result.bowlingT20.extraRuns += extras;
                    result.bowlingT20.totalBallsBowled++;
                    if(wicketKind != NULL)
                    {
                        result.bowlingT20.totalWickets++;
                        if(strcmp(wicketKind, "bowled")==0)
                        {
                            result.bowlingT20.totalBowledOuts++;
                        }
                        else if(strcmp(wicketKind, "lbw")==0)
                        {
                            result.bowlingT20.totalLBWs++;
                        }
                        else if(strcmp(wicketKind, "caught")==0)
                        {
                            result.bowlingT20.totalCatchOuts++;
                        }
                    }
                }
                if(test)
                {
                    result.bowlingTest.totalRunsConceded += runsOnBall;
                    result.bowlingTest.extraRuns += extras;
                    result.bowlingTest.totalBallsBowled++;
                    if(wicketKind != NULL)
                    {

                        result.bowlingTest.totalWickets++;
                        if(strcmp(wicketKind, "bowled")==0)
                        {
                            result.bowlingTest.totalBowledOuts++;
                        }
                        else if(strcmp(wicketKind, "lbw")==0)
                        {
                            result.bowlingTest.totalLBWs++;
                        }
                        else if(strcmp(wicketKind, "caught")==0)
                        {
                            result.bowlingTest.totalCatchOuts++;
                        }
                    }
                }
            }
                
            
            
        }
        //total overs bowled
        result.bowlingODI.totalOversBowled += result.bowlingODI.totalBallsBowled/6;
        result.bowlingT20.totalOversBowled += result.bowlingT20.totalBallsBowled/6;
        result.bowlingTest.totalOversBowled += result.bowlingTest.totalBallsBowled/6;

        //economy
        if(result.bowlingODI.totalOversBowled !=0)
            result.bowlingODI.economy = ((double)result.bowlingODI.totalRunsConceded+(double)result.bowlingODI.extraRuns)/(double)result.bowlingODI.totalOversBowled;
        if(result.bowlingT20.totalOversBowled !=0)
            result.bowlingT20.economy = ((double)result.bowlingT20.totalRunsConceded+(double)result.bowlingT20.extraRuns)/(double)result.bowlingT20.totalOversBowled;
        if(result.bowlingTest.totalOversBowled !=0)
            result.bowlingTest.economy = ((double)result.bowlingTest.totalRunsConceded+(double)result.bowlingTest.extraRuns)/(double)result.bowlingTest.totalOversBowled;
        //average
        if(result.battingODI.totalDismissals != 0)
            result.battingODI.totalAverage = (double)result.battingODI.totalRuns/(double)result.battingODI.totalDismissals;
        if(result.battingT20.totalDismissals != 0)
            result.battingT20.totalAverage = (double)result.battingT20.totalRuns/(double)result.battingT20.totalDismissals;
        if(result.battingTest.totalDismissals != 0)
           result.battingTest.totalAverage = (double)result.battingTest.totalRuns/(double)result.battingTest.totalDismissals;

        // Strike Rate
        if(result.battingODI.totalBallsFaced != 0)
            result.battingODI.totalStrikeRate = ((double)result.battingODI.totalRuns/(double)result.battingODI.totalBallsFaced)*100;
        if(result.battingT20.totalBallsFaced != 0)
            result.battingT20.totalStrikeRate = ((double)result.battingT20.totalRuns/(double)result.battingT20.totalBallsFaced)*100;
        if(result.battingTest.totalBallsFaced != 0)
           result.battingTest.totalStrikeRate = ((double)result.battingTest.totalRuns/(double)result.battingTest.totalBallsFaced*100);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return result;
    }
}