import axios from 'axios';
import { supabase } from './supabase';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    // Get session synchronously if possible, or handle auth in individual requests
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Helper function to create authenticated requests
export const createAuthenticatedRequest = async () => {
  try {
    const { data: sessionData } = await supabase.auth.getSession();
    
    if (sessionData.session?.access_token) {
      return {
        headers: {
          Authorization: `Bearer ${sessionData.session.access_token}`,
        },
      };
    }
  } catch (error) {
    console.error('Error getting session for API request:', error);
  }
  
  return { headers: {} };
};

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      console.error('Unauthorized access - redirecting to login');
      // You could add logic here to redirect to login
    } else if (error.response?.status >= 500) {
      console.error('Server error:', error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    }
    
    return Promise.reject(error);
  }
);

export default api;
