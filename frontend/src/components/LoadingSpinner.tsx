import { Activity } from 'lucide-react';

export default function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-500/20 rounded-full mb-6">
          <Activity className="h-8 w-8 text-orange-500 animate-pulse" />
        </div>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto mb-4"></div>
        <h1 className="text-2xl font-bold text-white mb-2">
          NBA <span className="text-orange-500">IQ</span>
        </h1>
        <p className="text-slate-400">Loading your analytics dashboard...</p>
      </div>
    </div>
  );
}
