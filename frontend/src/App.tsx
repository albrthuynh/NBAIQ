import React, { useState } from 'react';
import Navigation from '../src/components/Navigation';
import Home from '../src/components/Home';
import MatchPrediction from '../src/components/MatchPrediction';
import MVPAnalysis from '../src/components/MVPAnalysis';
import Analytics from '../src/components/Analytics';
import TeamComparison from '../src/components/TeamComparison';
import Footer from '../src/components/Footer';
import type { Team } from '../src/types/index';
import { teams, mvpCandidates } from '../src/data/mockData';

function App() {
  const [activeSection, setActiveSection] = useState('home');
  const [selectedTeam1, setSelectedTeam1] = useState<Team | null>(null);
  const [selectedTeam2, setSelectedTeam2] = useState<Team | null>(null);

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'home':
        return <Home setActiveSection={setActiveSection} />;
      case 'predict':
        return (
          <MatchPrediction 
            teams={teams}
            selectedTeam1={selectedTeam1}
            selectedTeam2={selectedTeam2}
            setSelectedTeam1={setSelectedTeam1}
            setSelectedTeam2={setSelectedTeam2}
          />
        );
      case 'mvp':
        return <MVPAnalysis mvpCandidates={mvpCandidates} />;
      case 'analytics':
        return <Analytics />;
      case 'compare':
        return (
          <TeamComparison 
            selectedTeam1={selectedTeam1}
            selectedTeam2={selectedTeam2}
          />
        );
      default:
        return <Home setActiveSection={setActiveSection} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
      <Navigation activeSection={activeSection} setActiveSection={setActiveSection} />
      
      <main className="py-8 px-4 sm:px-6 lg:px-8">
        {renderActiveSection()}
      </main>

      <Footer />
    </div>
  );
}

export default App;