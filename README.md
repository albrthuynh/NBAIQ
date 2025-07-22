# NBA IQ - NBA Analytics & Machine Learning Platform

A comprehensive NBA analytics platform that uses machine learning to provide match predictions, MVP analysis, team comparisons, and detailed player statistics. Built with React, TypeScript, Python Flask, and Supabase. 

## 🏀 Features

- **Match Prediction**: AI-powered game outcome predictions using advanced ML algorithms
- **MVP Analysis**: Statistical analysis to predict Most Valuable Player candidates
- **Team Comparison**: Side-by-side team statistics and performance metrics
- **Interactive Analytics**: Real-time data visualization and insights
- **User Authentication**: Secure login and personalized experience
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS

## 🛠️ Tech Stack

### Frontend
- **React 19** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Radix UI** for accessible components
- **Axios** for API communication
- **Lucide React** for icons

### Backend
- **Python Flask** RESTful API
- **Machine Learning**: scikit-learn, XGBoost, pandas, numpy
- **Supabase** for database and authentication
- **Flask-CORS** for cross-origin requests

### Database
- **Supabase** (PostgreSQL) for user data and analytics storage

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **npm** or **yarn**
- **Python** (3.8 or higher)
- **pip** (Python package installer)
- **Supabase Account** (for database and authentication)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/albrthuynh/NBAIQ.git
cd AA-Hackathon
```

### 2. Supabase Setup

1. Create a free account at [Supabase](https://supabase.com)
2. Create a new project
3. Go to **Settings > API** and copy:
   - Project URL
   - Anon/Public Key
   - Service Role Key (keep this secret!)

### 3. Environment Configuration

Create a `.env.local` file in the **root directory**:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE=your_supabase_service_role_key
```

### 4. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

**Requirements include:**
- pandas>=1.5.0
- scikit-learn>=1.2.0
- xgboost>=1.7.0
- numpy>=1.21.0
- flask
- flask-cors
- supabase
- python-dotenv

### 5. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd ../frontend
npm install
```

## 🏃‍♂️ Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The Flask API will run on `http://localhost:5000`

### Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The React app will run on `http://localhost:5173` (or `http://localhost:5174` if 5173 is occupied)

## 📁 Project Structure

```
AA-Hackathon/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── prediction_improved.py # ML prediction models
│   ├── Games.csv             # NBA games dataset
│   ├── Team Stats Per 100 Poss.csv # Team statistics
│   ├── requirements.txt      # Python dependencies
│   └── test_api.py          # API tests
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── contexts/        # React contexts (Auth)
│   │   ├── lib/            # Utility libraries
│   │   ├── types/          # TypeScript type definitions
│   │   └── data/           # Mock data
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
└── README.md              # This file
```

## 🔧 Configuration

### Port Configuration

- **Backend**: Runs on port 5000 by default
- **Frontend**: Runs on port 5173 by default (auto-increments if occupied)

To change the frontend port, modify `vite.config.ts`:

```typescript
export default defineConfig({
  // ... other config
  server: {
    port: 3000, // Your desired port
    strictPort: true, // Fail if port is occupied
  },
})
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173`
- `http://localhost:5174`

Update the CORS configuration in `backend/app.py` if using different ports.

## 🧪 Testing

Run backend tests:

```bash
cd backend
python -m pytest test_api.py
```

Or use the provided test script:

```bash
cd backend
chmod +x run_tests.sh
./run_tests.sh
```

## 📊 Data Sources

The application uses NBA statistical data including:
- Historical game results
- Team performance metrics (per 100 possessions)
- Player statistics
- Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Port conflicts**: If you get port errors, check what's running on your ports with `lsof -i :5173`
2. **Supabase connection errors**: Verify your environment variables are correctly set
3. **CORS errors**: Ensure the backend CORS configuration matches your frontend URL
4. **Python package errors**: Make sure you're using Python 3.8+ and have installed all requirements

### Support

If you encounter any issues, please:
1. Check the console for error messages
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed
4. Create an issue on GitHub with detailed error information

---

Built with ❤️ for NBA analytics enthusiasts