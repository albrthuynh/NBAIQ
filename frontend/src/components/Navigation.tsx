import { Activity, LogOut, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface NavigationProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
}

export default function Navigation({ activeSection, setActiveSection }: NavigationProps) {
  const { user, logout } = useAuth();
  
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'predict', label: 'Match Prediction' },
    { id: 'mvp', label: 'MVP Analysis' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'compare', label: 'Team Comparison' },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-orange-400" />
            <span className="text-2xl font-bold text-white">NBA <span className="text-orange-400">IQ</span></span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveSection(item.id)}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeSection === item.id 
                    ? 'text-orange-400 bg-orange-400/10' 
                    : 'text-slate-300 hover:text-white'
                }`}
              >
                {item.label}
              </button>
            ))}
            
            {/* User Menu */}
            <div className="flex items-center space-x-4 ml-8 pl-8 border-l border-slate-700">
              <div className="flex items-center space-x-2 text-slate-300">
                <User className="h-4 w-4" />
                <span className="text-sm">
                  {user?.firstName} {user?.lastName}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-colors"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}