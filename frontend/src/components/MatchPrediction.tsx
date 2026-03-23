import React, { useState } from 'react';
import { Target, Zap, Trophy } from 'lucide-react';
import axios from 'axios';
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
  const [homeWinProbability, setHomeWinProbability] = useState<number | null>(null);
  const [awayWinProbability, setAwayWinProbability] = useState<number | null>(null);
  const [homeSeason, setHomeSeason] = useState<number>(2025);
  const [awaySeason, setAwaySeason] = useState<number>(2025);
  const [isLoadingPrediction, setIsLoadingPrediction] = useState(false);
  const [predictionError, setPredictionError] = useState<string | null>(null);

  const handleMatchPrediction = async () => {
    if (!selectedTeam1 || !selectedTeam2) return;

    setPredictionError(null);
    setIsLoadingPrediction(true);

    try {
      const response = await axios.post('/api/predict', {
        home_team: `${selectedTeam1.city} ${selectedTeam1.name}`,
        home_season: homeSeason,
        away_team: `${selectedTeam2.city} ${selectedTeam2.name}`,
        away_season: awaySeason,
      });

      const prediction = response.data;
      setMatchPrediction(prediction.predicted_winner);
      setHomeWinProbability(Number(prediction.home_win_probability) * 100);
      setAwayWinProbability(Number(prediction.away_win_probability) * 100);
    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        setPredictionError(error.response?.data?.error || 'Failed to fetch prediction');
      } else {
        setPredictionError('Failed to fetch prediction');
      }
      setMatchPrediction(null);
      setHomeWinProbability(null);
      setAwayWinProbability(null);
    } finally {
      setIsLoadingPrediction(false);
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

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
                    <label className="text-left">
                      <div className="text-sm text-slate-300 mb-1">
                        {selectedTeam1.name} season (home)
                      </div>
                      <input
                        type="number"
                        value={homeSeason}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setHomeSeason(Number(e.target.value))}
                        className="w-full px-3 py-2 rounded-lg border border-slate-600 bg-slate-800/40 text-white"
                      />
                    </label>
                    <label className="text-left">
                      <div className="text-sm text-slate-300 mb-1">
                        {selectedTeam2.name} season (away)
                      </div>
                      <input
                        type="number"
                        value={awaySeason}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAwaySeason(Number(e.target.value))}
                        className="w-full px-3 py-2 rounded-lg border border-slate-600 bg-slate-800/40 text-white"
                      />
                    </label>
                  </div>
                  
                  <button
                    onClick={handleMatchPrediction}
                    disabled={isLoadingPrediction}
                    className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105"
                  >
                    <Zap className="inline mr-2 h-5 w-5" />
                    {isLoadingPrediction ? 'Generating...' : 'Generate Prediction'}
                  </button>
                </div>

                {predictionError && (
                  <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
                    <div className="text-red-300 text-sm">{predictionError}</div>
                  </div>
                )}

                {matchPrediction && (
                  <div className="mt-6 p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Trophy className="h-5 w-5 text-green-400" />
                      <span className="text-green-400 font-semibold">Predicted Winner:</span>
                    </div>
                    <div className="text-white text-lg mt-1">{matchPrediction}</div>
                    {homeWinProbability !== null && awayWinProbability !== null && (
                      <div className="text-slate-200 mt-3 space-y-1">
                        <div>{selectedTeam1.name} win probability: {homeWinProbability.toFixed(1)}%</div>
                        <div>{selectedTeam2.name} win probability: {awayWinProbability.toFixed(1)}%</div>
                      </div>
                    )}
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