import React from 'react';
import type { Player } from '../types/index';

interface MVPAnalysisProps {
  mvpCandidates: Player[];
}

export default function MVPAnalysis({ mvpCandidates }: MVPAnalysisProps) {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">MVP Prediction Analysis</h2>
        <p className="text-xl text-slate-400">AI-powered analysis of MVP candidates based on performance metrics</p>
      </div>

      <div className="grid gap-6">
        {mvpCandidates.map((player, index) => (
          <div key={player.id} className="bg-gradient-to-r from-slate-800/50 to-slate-900/50 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                  index === 0 ? 'bg-yellow-500 text-black' : 
                  index === 1 ? 'bg-slate-400 text-black' : 
                  index === 2 ? 'bg-amber-600 text-white' : 'bg-slate-600 text-white'
                }`}>
                  {index + 1}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white">{player.name}</h3>
                  <p className="text-slate-400">{player.team}</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-orange-400">{player.mvpProbability}%</div>
                <div className="text-sm text-slate-400">MVP Probability</div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center p-3 bg-slate-800/50 rounded-lg">
                <div className="text-xl font-bold text-white">{player.ppg}</div>
                <div className="text-sm text-slate-400">PPG</div>
              </div>
              <div className="text-center p-3 bg-slate-800/50 rounded-lg">
                <div className="text-xl font-bold text-white">{player.rpg}</div>
                <div className="text-sm text-slate-400">RPG</div>
              </div>
              <div className="text-center p-3 bg-slate-800/50 rounded-lg">
                <div className="text-xl font-bold text-white">{player.apg}</div>
                <div className="text-sm text-slate-400">APG</div>
              </div>
            </div>

            <div className="relative">
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-orange-500 to-yellow-500 transition-all duration-1000"
                  style={{ width: `${player.mvpProbability}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}