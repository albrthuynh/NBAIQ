import React from 'react';
import { 
  Activity, 
  ChevronRight,
  Target,
  Award,
  BarChart3,
  Users
} from 'lucide-react';

interface HomeProps {
  setActiveSection: (section: string) => void;
}

export default function Home({ setActiveSection }: HomeProps) {
  const features = [
    {
      icon: Target,
      title: 'Match Prediction',
      description: 'AI-powered predictions for any team matchup with confidence metrics'
    },
    {
      icon: Award,
      title: 'MVP Analysis',
      description: 'Predict MVP winners based on advanced statistical models'
    },
    {
      icon: BarChart3,
      title: 'All-Time Rankings',
      description: 'Historical analytics for teams and players across all seasons'
    },
    {
      icon: Users,
      title: 'Team Comparison',
      description: 'Interactive tools to compare team stats and performance metrics'
    }
  ];

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-orange-900/20 to-slate-900"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="p-4 bg-orange-500/20 rounded-full backdrop-blur-sm border border-orange-500/30">
                <Activity className="h-12 w-12 text-orange-400" />
              </div>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 tracking-tight">
              NBA <span className="text-orange-400">IQ</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Advanced Basketball Analytics Platform powered by Artificial Intelligence
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => setActiveSection('predict')}
                className="px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl"
              >
                Start Predicting
                <ChevronRight className="inline ml-2 h-5 w-5" />
              </button>
              <button 
                onClick={() => setActiveSection('analytics')}
                className="px-8 py-4 bg-slate-800/50 hover:bg-slate-700/50 text-white font-semibold rounded-lg border border-slate-600 backdrop-blur-sm transition-all duration-300"
              >
                Explore Analytics
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white mb-4">Powerful Analytics Suite</h2>
          <p className="text-xl text-slate-400">Comprehensive tools for basketball analysis and prediction</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="group p-6 bg-slate-800/50 rounded-xl border border-slate-700 hover:border-orange-500/50 transition-all duration-300 hover:transform hover:scale-105">
              <div className="p-3 bg-orange-500/20 rounded-lg w-fit mb-4 group-hover:bg-orange-500/30 transition-colors">
                <feature.icon className="h-8 w-8 text-orange-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-slate-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}