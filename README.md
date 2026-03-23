# NBA IQ

NBA IQ is an NBA analytics and machine learning platform built with React, TypeScript, Flask, and Supabase.

## Features

- Match prediction with backend ML inference
- MVP analysis and team comparison views
- Authenticated user flow with Supabase
- Responsive frontend built with Tailwind CSS

## Tech Stack

### Frontend
- React 19 + TypeScript
- Vite
- Tailwind CSS
- Axios

### Backend
- Flask
- scikit-learn, XGBoost, pandas, numpy
- Supabase + Flask-CORS

## Prerequisites

- Node.js 18+
- npm
- Python 3.8+
- pip
- Supabase project credentials

## Setup

### 1) Clone

```bash
git clone https://github.com/albrthuynh/NBAIQ.git
cd NBAIQ
```

### 2) Environment variables

Create `.env.local` in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE=your_supabase_service_role_key
```

### 3) Backend

```bash
cd backend
pip install -r requirements.txt
```

### 4) Frontend

```bash
cd frontend
npm install
```

## Run

### Backend

```bash
cd backend
python app.py
```

Backend runs at `http://localhost:5000`.

### Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at `http://localhost:5173` (or `http://localhost:5174` if occupied).

## API

### `POST /api/predict`

Request body:

```json
{
  "home_team": "Chicago Bulls",
  "home_season": 2025,
  "away_team": "Indiana Pacers",
  "away_season": 2025
}
```

Response body:

```json
{
  "home_team": "Chicago Bulls",
  "home_season": 2025,
  "away_team": "Indiana Pacers",
  "away_season": 2025,
  "predicted_winner": "Chicago Bulls",
  "home_win_probability": 0.7,
  "away_win_probability": 0.3,
  "model": "RandomForestClassifier"
}
```

## Testing

```bash
cd backend
python -m pytest test_api.py
```

If `pytest` is missing in your environment:

```bash
pip install pytest
```

## Notes

- Backend CORS currently allows `http://localhost:5173` and `http://localhost:5174`.
- Update allowed origins in `backend/app.py` if your frontend runs on a different port.