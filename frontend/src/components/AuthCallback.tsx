import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from './LoadingSpinner';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        // Get the code and other params from the URL
        const code = searchParams.get('code');
        const error = searchParams.get('error');
        const errorDescription = searchParams.get('error_description');

        if (error) {
          console.error('Auth callback error:', error, errorDescription);
          setStatus('error');
          setMessage(errorDescription || 'Authentication failed');
          return;
        }

        if (code) {
          // Exchange the code for a session
          const { data, error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
          
          if (exchangeError) {
            console.error('Session exchange error:', exchangeError);
            setStatus('error');
            setMessage('Failed to confirm email. Please try again.');
            return;
          }

          if (data.user) {
            console.log('Email confirmed successfully for user:', data.user.email);
            setStatus('success');
            setMessage('Email confirmed successfully! Redirecting...');
            
            // Redirect to the app after a short delay
            setTimeout(() => {
              navigate('/app');
            }, 2000);
          }
        } else {
          setStatus('error');
          setMessage('Invalid confirmation link');
        }
      } catch (err) {
        console.error('Auth callback error:', err);
        setStatus('error');
        setMessage('An unexpected error occurred');
      }
    };

    handleAuthCallback();
  }, [searchParams, navigate]);

  // If user is already authenticated, redirect them
  useEffect(() => {
    if (user && status === 'loading') {
      navigate('/app');
    }
  }, [user, navigate, status]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900">
      <div className="bg-slate-800 p-8 rounded shadow-md text-center max-w-md">
        {status === 'loading' && (
          <>
            <LoadingSpinner />
            <h2 className="text-2xl font-bold text-white mb-4">
              Confirming your email...
            </h2>
            <p className="text-slate-300">
              Please wait while we verify your account.
            </p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="text-green-400 text-4xl mb-4">✓</div>
            <h2 className="text-2xl font-bold text-white mb-4">
              Email Confirmed!
            </h2>
            <p className="text-slate-300 mb-4">
              {message}
            </p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="text-red-400 text-4xl mb-4">✗</div>
            <h2 className="text-2xl font-bold text-white mb-4">
              Confirmation Failed
            </h2>
            <p className="text-red-400 mb-4">
              {message}
            </p>
            <button
              onClick={() => navigate('/')}
              className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded"
            >
              Back to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
}
