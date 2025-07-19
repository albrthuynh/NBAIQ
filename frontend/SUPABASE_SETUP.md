# Supabase Setup Instructions

## 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/log in
2. Click "New Project"
3. Choose your organization and fill in project details
4. Wait for the project to be created

## 2. Get Your Supabase Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy your **Project URL** and **anon/public key**

## 3. Set Up Environment Variables

1. Create a `.env.local` file in your frontend directory:
```bash
cp .env.example .env.local
```

2. Replace the placeholder values with your actual Supabase credentials:
```
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

## 4. Configure Authentication

In your Supabase dashboard:

1. Go to **Authentication** → **Settings**
2. Configure your site URL (for development: `http://localhost:5173`)
3. Optionally configure social auth providers (Google, GitHub, etc.)

## 5. User Management

Your users will be automatically stored in Supabase's built-in `auth.users` table. The `user_metadata` field will contain the firstName and lastName.

## 6. Security

- The anon key is safe to use in frontend code
- Supabase handles all security aspects including JWT tokens
- User sessions are automatically managed
- Row Level Security (RLS) can be configured for your custom tables

## Features Implemented

✅ **Email/Password Authentication**
- User registration with first name and last name
- User login
- Automatic session management
- Logout functionality

✅ **Security Features**
- Secure client-side authentication
- Automatic JWT token handling
- Session persistence across browser refreshes

✅ **User Experience**
- Loading states during auth operations
- Error handling and display
- Form validation
- Password visibility toggles

## Next Steps

1. **Email Verification**: Configure email templates in Supabase
2. **Password Reset**: Add forgot password functionality
3. **Social Auth**: Enable Google/GitHub login
4. **User Profiles**: Create a profiles table for additional user data
5. **Protected API Routes**: Secure your backend endpoints
