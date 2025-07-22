import { useState } from "react";
import { AuthProvider } from "./contexts/AuthContext";
import Navigation from "../src/components/Navigation";
import Home from "../src/components/Home";
import MatchPrediction from "../src/components/MatchPrediction";
import MVPAnalysis from "../src/components/MVPAnalysis";
import Analytics from "../src/components/Analytics";
import TeamComparison from "../src/components/TeamComparison";
import Footer from "../src/components/Footer";
import ProtectedRoute from "../src/components/ProtectedRoute";
import type { Team } from "../src/types/index";
import { teams, mvpCandidates } from "../src/data/mockData";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ForgotPasswordPage from "./components/ForgotPassword";
import ResetPasswordPage from "./components/ResetPassword";
import AuthPage from "./components/Auth";
import EmailConfirmation from "./components/EmailConfirmation";
import axios from "axios";

// Connect Frontend to Backend
axios.defaults.baseURL = "http://localhost:5000";

function AppContent() {
  const [activeSection, setActiveSection] = useState("home");
  const [selectedTeam1, setSelectedTeam1] = useState<Team | null>(null);
  const [selectedTeam2, setSelectedTeam2] = useState<Team | null>(null);

  const renderActiveSection = () => {
    switch (activeSection) {
      case "home":
        return <Home setActiveSection={setActiveSection} />;
      case "predict":
        return (
          <MatchPrediction
            teams={teams}
            selectedTeam1={selectedTeam1}
            selectedTeam2={selectedTeam2}
            setSelectedTeam1={setSelectedTeam1}
            setSelectedTeam2={setSelectedTeam2}
          />
        );
      case "mvp":
        return <MVPAnalysis mvpCandidates={mvpCandidates} />;
      case "analytics":
        return <Analytics />;
      case "compare":
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
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
        <Navigation
          activeSection={activeSection}
          setActiveSection={setActiveSection}
        />

        <main className="py-8 px-4 sm:px-6 lg:px-8">
          {renderActiveSection()}
        </main>

        <Footer />
      </div>
    </ProtectedRoute>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AuthPage />} />
          <Route path="/confirm-email" element={<EmailConfirmation />} />
          <Route path="/app/*" element={<AppContent />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage/>}/>
          <Route path="/reset-password" element={<ResetPasswordPage/>}/>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
