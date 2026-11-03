// #include <string>
// #include <filesystem>
// #include <iostream>
// #include <fstream>
// #include <vector>
// #include <algorithm>
// #include <random>
// #include <array>
// #include "PVP.h"
// #include "PVG.h"
// #include "nlohmann/json.hpp"
// #include <filesystem>
// #include <sqlite3.h>

// namespace PVG
// {
//     std::vector <PVGResult> queryPVG(std::string namePlayer1, std::string groundName)
//     {
//         PVGResult result; 
//         sqlite3* db; 
//         sqlite3_open("allCricketMatches.db", &db);
//         sqlite3_stmt* stmt;
//         sqlite3_prepare_v2(db,
//             "SELECT match_id, matchType, batter, bowler, runs_batter, extras, wicket_kind "
//             "FROM deliveries WHERE (batter = ? OR bowler = ?) AND matchVenue = ?",
//             -1, &stmt, nullptr);
//         sqlite3_bind_text(stmt,1,namePlayer1.c_str(),-1,SQLITE_STATIC);
//         sqlite3_bind_text(stmt,1,namePlayer1.c_str(),-1,SQLITE_STATIC);
//         sqlite3_bind_text(stmt,1,groundName.c_str(),-1,SQLITE_STATIC);
//         std::string lastMatchId = "";
//         bool test = false;
//         bool odi = false;
//         bool t20 = false;
//          while (sqlite3_step(stmt) == SQLITE_ROW) 
//         {
//             if(strcmp(batter, namePlayer1) == 0)
//             {
//                 std::string currentMatchId = (const char*)sqlite3_column_text(stmt, 0);
//                 test = false;
//                 odi = false;
//                 t20 = false;
//                 const char* matchType = (const char*)sqlite3_column_text(stmt,2);
//                 if(strcmp(matchType, "ODM") == 0 || strcmp(matchType, "ODI") == 0)
//                 {
//                     result.battingODI.totalMatchesPlayed++;
//                     odi = true;
//                 }
//                 if(strcmp(matchType, "IT20") == 0 || strcmp(matchType, "T20") == 0)
//                 {
//                     result.battingT20.totalMatchesPlayed++;
//                     t20 = true;
//                 }
//                 if(strcmp(matchType, "Test") == 0 || strcmp(matchType, "MDM") == 0)
//                 {
//                     result.battingTest.totalMatchesPlayed++;
//                     test = true;
//                 }
//                 lastMatchId = currentMatchId;
//             }
//         }

//     }
// }