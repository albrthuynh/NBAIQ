import React, { useState } from 'react';
import { Target, Zap, Trophy } from 'lucide-react';
import type { Team } from '../types/index';

interface MatchPredictionProps {
  teams: Team[];
  selectedTeam1: Team | null;
  selectedTeam2: Team | null;
  setSelectedTeam1: (team: Team | null) => void;
  setSelectedTeam2: (team: Team | null) => void;
}

export default function MatchPrediction({ 
  teams, 
  selectedTeam1, 
  selectedTeam2, 
  setSelectedTeam1, 
  setSelectedTeam2 
}: MatchPredictionProps) {
  const [matchPrediction, setMatchPrediction] = useState<string | null>(null);

  const handleMatchPrediction = () => {
    if (selectedTeam1 && selectedTeam2) {
      const team1Score = selectedTeam1.offensiveRating - selectedTeam2.defensiveRating + Math.random() * 10;
      const team2Score = selectedTeam2.offensiveRating - selectedTeam1.defensiveRating + Math.random() * 10;
      const winner = team1Score > team2Score ? selectedTeam1 : selectedTeam2;
      const confidence = Math.round(Math.abs(team1Score - team2Score) * 5 + 60);
      setMatchPrediction(`${winner.city} ${winner.name} - ${confidence}% confidence`);
    }
  };

  const TeamSelector = ({ 
    title, 
    selectedTeam, 
    onTeamSelect 
  }: { 
    title: string; 
    selectedTeam: Team | null; 
    onTeamSelect: (team: Team) => void; 
  }) => (
    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
      <h3 className="text-xl font-semibold text-white mb-4">{title}</h3>
      <div className="grid gap-3">
        {teams.map((team) => (
          <button
            key={team.id}
            onClick={() => onTeamSelect(team)}
            className={`p-4 rounded-lg border transition-all text-left ${
              selectedTeam?.id === team.id
                ? 'border-orange-500 bg-orange-500/10'
                : 'border-slate-600 bg-slate-800/30 hover:border-slate-500'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{team.logo}</span>
                <div>
                  <div className="text-white font-medium">{team.city} {team.name}</div>
                  <div className="text-sm text-slate-400">{team.wins}-{team.losses}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-slate-400">Off: {team.offensiveRating}</div>
                <div className="text-sm text-slate-400">Def: {team.defensiveRating}</div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">Match Outcome Prediction</h2>
        <p className="text-xl text-slate-400">Select two teams to predict the winner using AI analytics</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Team Selection */}
        <div className="space-y-6">
          <TeamSelector 
            title="Team 1" 
            selectedTeam={selectedTeam1} 
            onTeamSelect={setSelectedTeam1} 
          />
          <TeamSelector 
            title="Team 2" 
            selectedTeam={selectedTeam2} 
            onTeamSelect={setSelectedTeam2} 
          />
        </div>

        {/* Prediction Results */}
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 rounded-xl p-6 border border-slate-700">
            <h3 className="text-xl font-semibold text-white mb-6">Prediction Analysis</h3>
            
            {selectedTeam1 && selectedTeam2 ? (
              <div className="space-y-4">
                <div className="text-center py-6">
                  <div className="flex items-center justify-center space-x-4 mb-4">
                    <div className="text-center">
                      <span className="text-3xl">{selectedTeam1.logo}</span>
                      <div className="text-white font-medium">{selectedTeam1.name}</div>
                    </div>
                    <div className="text-2xl text-slate-400">VS</div>
                    <div className="text-center">
                      <span className="text-3xl">{selectedTeam2.logo}</span>
                      <div className="text-white font-medium">{selectedTeam2.name}</div>
                    </div>
                  </div>
                  
                  <button
                    onClick={handleMatchPrediction}
                    className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105"
                  >
                    <Zap className="inline mr-2 h-5 w-5" />
                    Generate Prediction
                  </button>
                </div>

                {matchPrediction && (
                  <div className="mt-6 p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Trophy className="h-5 w-5 text-green-400" />
                      <span className="text-green-400 font-semibold">Predicted Winner:</span>
                    </div>
                    <div className="text-white text-lg mt-1">{matchPrediction}</div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-slate-400">
                <Target className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Select two teams to generate a prediction</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}