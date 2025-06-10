import React from 'react';
import { TrendingUp, Star } from 'lucide-react';

export default function Analytics() {
  const bestOffensiveTeams = [
    { team: "2016-17 Warriors", rating: 115.6, ppg: 115.9 },
    { team: "2020-21 Nets", rating: 118.1, ppg: 117.3 },
    { team: "2017-18 Rockets", rating: 112.4, ppg: 112.4 },
    { team: "2018-19 Warriors", rating: 114.5, ppg: 117.7 }
  ];

  const bestThreePointShooters = [
    { player: "Stephen Curry", percentage: 42.8, made: 402 },
    { player: "Klay Thompson", percentage: 41.9, made: 276 },
    { player: "Steve Nash", percentage: 42.8, made: 1685 },
    { player: "Reggie Miller", percentage: 39.5, made: 2560 }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-12">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">All-Time Analytics</h2>
        <p className="text-xl text-slate-400">Historical performance analysis and rankings</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Best Offensive Teams */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
            <TrendingUp className="mr-3 h-6 w-6 text-orange-400" />
            Best Offensive Teams
          </h3>
          <div className="space-y-4">
            {bestOffensiveTeams.map((team, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-800/30 rounded-lg">
                <div>
                  <div className="text-white font-medium">{team.team}</div>
                  <div className="text-sm text-slate-400">Off Rating: {team.rating}</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-orange-400">{team.ppg}</div>
                  <div className="text-sm text-slate-400">PPG</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Best Three-Point Shooters */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
            <Star className="mr-3 h-6 w-6 text-orange-400" />
            Best 3-Point Shooters
          </h3>
          <div className="space-y-4">
            {bestThreePointShooters.map((player, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-800/30 rounded-lg">
                <div>
                  <div className="text-white font-medium">{player.player}</div>
                  <div className="text-sm text-slate-400">{player.made} Career 3PM</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-orange-400">{player.percentage}%</div>
                  <div className="text-sm text-slate-400">3P%</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}