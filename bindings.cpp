#include <pybind11/pybind11.h>
#include "PVP.h"

PYBIND11_MODULE(statsPVP,m)
{

        // int totalWickets = 0;
        // int totalOversBowled = 0;
        // int totalCatchOuts = 0; 
        // int totalLBWs = 0;
        // int totalBowledOuts = 0;

        // //Batsman Stats
        // int totalFours = 0;
        // int totalSixes = 0;
        // double totalAverage = 0;
        // double totalStrikeRate = 0;

        
        // //Common Stats
        // int totalRuns = 0;
        // int totalBallsFaced = 0;
        // int totalMatchesPlayed = 0;

    pybind11::class_<PVP::AggregateStats>(m,"AggregateStats")
        .def_readonly("totalWickets",&PVP::AggregateStats::totalWickets)
        .def_readonly("totalOversBowled",&PVP::AggregateStats::totalOversBowled)
        .def_readonly("totalCatchOuts",&PVP::AggregateStats::totalCatchOuts)
        .def_readonly("totalLBWs",&PVP::AggregateStats::totalLBWs)
        .def_readonly("totalBowledOuts",&PVP::AggregateStats::totalBowledOuts)
        .def_readonly("totalFours",&PVP::AggregateStats::totalFours)
        .def_readonly("totalSixes",&PVP::AggregateStats::totalSixes)
        .def_readonly("totalAverage",&PVP::AggregateStats::totalAverage)
        .def_readonly("totalStrikeRate",&PVP::AggregateStats::totalStrikeRate)
        .def_readonly("totalRuns",&PVP::AggregateStats::totalRuns)
        .def_readonly("totalBallsFaced",&PVP::AggregateStats::totalBallsFaced)
        .def_readonly("totalMatchesPlayed",&PVP::AggregateStats::totalMatchesPlayed);

        m.def("query",&PVP::query);
}