import React from 'react';
import { Users } from 'lucide-react';
import type { Team } from '../types/index';

interface TeamComparisonProps {
  selectedTeam1: Team | null;
  selectedTeam2: Team | null;
}

export default function TeamComparison({ selectedTeam1, selectedTeam2 }: TeamComparisonProps) {
  if (!selectedTeam1 || !selectedTeam2) {
    return (
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">Team Comparison Tool</h2>
          <p className="text-xl text-slate-400">Advanced statistical comparison between any two teams</p>
        </div>

        <div className="bg-slate-800/50 rounded-xl p-12 border border-slate-700 text-center">
          <Users className="h-16 w-16 mx-auto mb-4 text-slate-500" />
          <p className="text-slate-400 text-lg">Select teams from the Match Prediction section to compare them here</p>
        </div>
      </div>
    );
  }

  const comparisonMetrics = [
    {
      name: 'Offensive Rating',
      team1Value: selectedTeam1.offensiveRating,
      team2Value: selectedTeam2.offensiveRating,
      higherIsBetter: true
    },
    {
      name: 'Defensive Rating',
      team1Value: selectedTeam1.defensiveRating,
      team2Value: selectedTeam2.defensiveRating,
      higherIsBetter: false
    },
    {
      name: 'Win Percentage',
      team1Value: (selectedTeam1.wins / (selectedTeam1.wins + selectedTeam1.losses)) * 100,
      team2Value: (selectedTeam2.wins / (selectedTeam2.wins + selectedTeam2.losses)) * 100,
      higherIsBetter: true,
      isPercentage: true
    }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">Team Comparison Tool</h2>
        <p className="text-xl text-slate-400">Advanced statistical comparison between any two teams</p>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <div className="text-center">
            <span className="text-4xl mb-2 block">{selectedTeam1.logo}</span>
            <h3 className="text-2xl font-bold text-white">{selectedTeam1.city} {selectedTeam1.name}</h3>
            <p className="text-slate-400">{selectedTeam1.wins}-{selectedTeam1.losses}</p>
          </div>
          <div className="text-center">
            <span className="text-4xl mb-2 block">{selectedTeam2.logo}</span>
            <h3 className="text-2xl font-bold text-white">{selectedTeam2.city} {selectedTeam2.name}</h3>
            <p className="text-slate-400">{selectedTeam2.wins}-{selectedTeam2.losses}</p>
          </div>
        </div>

        <div className="space-y-6">
          {comparisonMetrics.map((metric, index) => {
            const team1Better = metric.higherIsBetter 
              ? metric.team1Value > metric.team2Value 
              : metric.team1Value < metric.team2Value;
            
            const team1Percentage = metric.higherIsBetter
              ? (metric.team1Value / (metric.team1Value + metric.team2Value)) * 100
              : (metric.team2Value / (metric.team1Value + metric.team2Value)) * 100;
            
            const team2Percentage = 100 - team1Percentage;

            return (
              <div key={index}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-white">{metric.name}</span>
                  <div className="flex space-x-4">
                    <span className={`font-bold ${team1Better ? 'text-green-400' : 'text-orange-400'}`}>
                      {metric.isPercentage ? `${metric.team1Value.toFixed(1)}%` : metric.team1Value}
                    </span>
                    <span className={`font-bold ${!team1Better ? 'text-green-400' : 'text-blue-400'}`}>
                      {metric.isPercentage ? `${metric.team2Value.toFixed(1)}%` : metric.team2Value}
                    </span>
                  </div>
                </div>
                <div className="relative h-4 bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    className="absolute left-0 top-0 h-full bg-orange-500 transition-all duration-1000"
                    style={{ width: `${team1Percentage}%` }}
                  ></div>
                  <div 
                    className="absolute right-0 top-0 h-full bg-blue-500 transition-all duration-1000"
                    style={{ width: `${team2Percentage}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}