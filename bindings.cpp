#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "PVP.h"
#include "PVG.h"
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
        .def_readonly("economy", &PVP::AggregateStats::economy)
        .def_readonly("extraRuns", &PVP::AggregateStats::extraRuns)
        .def_readonly("totalBallsFaced",&PVP::AggregateStats::totalBallsFaced)
        .def_readonly("totalMatchesPlayed",&PVP::AggregateStats::totalMatchesPlayed);

        m.def("queryPVP",&PVP::queryPVP);

        
    pybind11::class_<PVG::BatterAggregate>(m,"BatterAggregate")
        .def_readonly("totalRuns",&PVG::BatterAggregate::totalRuns)
        .def_readonly("totalBallsFaced",&PVG::BatterAggregate::totalBallsFaced)
        .def_readonly("totalFours",&PVG::BatterAggregate::totalFours)
        .def_readonly("totalSixes",&PVG::BatterAggregate::totalSixes)
        .def_readonly("totalMatchesPlayed",&PVG::BatterAggregate::totalMatchesPlayed)
        .def_readonly("totalDismissals",&PVG::BatterAggregate::totalDismissals)
        .def_readonly("totalCatchOuts",&PVG::BatterAggregate::totalCatchOuts)
        .def_readonly("totalLBWs",&PVG::BatterAggregate::totalLBWs)
        .def_readonly("totalBowledOuts",&PVG::BatterAggregate::totalBowledOuts)
        .def_readonly("totalAverage",&PVG::BatterAggregate::totalAverage)
        .def_readonly("totalStrikeRate",&PVG::BatterAggregate::totalStrikeRate);
    pybind11::class_<PVG::BowlerAggregate>(m,"BowlerAggregate")
        .def_readonly("totalRunsConceded", &PVG::BowlerAggregate::totalRunsConceded)
        .def_readonly("totalBallsBowled", &PVG::BowlerAggregate::totalBallsBowled)
        .def_readonly("totalOversBowled", &PVG::BowlerAggregate::totalOversBowled)
        .def_readonly("totalWickets", &PVG::BowlerAggregate::totalWickets)
        .def_readonly("totalCatchOuts", &PVG::BowlerAggregate::totalCatchOuts)
        .def_readonly("totalLBWs", &PVG::BowlerAggregate::totalLBWs)
        .def_readonly("totalBowledOuts", &PVG::BowlerAggregate::totalBowledOuts)
        .def_readonly("totalMatchesPlayed", &PVG::BowlerAggregate::totalMatchesPlayed)
        .def_readonly("extraRuns", &PVG::BowlerAggregate::extraRuns)
        .def_readonly("economy", &PVG::BowlerAggregate::economy);

    pybind11::class_<PVG::PVGResult>(m,"PVGResult")
        .def_readonly("battingTest", &PVG::PVGResult::battingTest)
        .def_readonly("battingODI", &PVG::PVGResult::battingODI)
        .def_readonly("battingT20", &PVG::PVGResult::battingT20)
        .def_readonly("bowlingTest", &PVG::PVGResult::bowlingTest)
        .def_readonly("bowlingODI", &PVG::PVGResult::bowlingODI)
        .def_readonly("bowlingT20", &PVG::PVGResult::bowlingT20);

        m.def("queryPVG",&PVG::queryPVG);




}
