# EthioGuide 🇪🇹

EthioGuide is an AI-powered web platform designed to promote Ethiopian cultural heritage and tourism.

The platform helps users discover historical sites, cultural places, and festivals in Ethiopia using AI-powered recommendations and an interactive map.

## Tech Stack
- Frontend: React + TypeScript
- Backend: Python (FastAPI)
- Database: MONGODB
- Maps: Leaflet.js

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- MongoDB Atlas account
- Google Gemini API Key

### Backend Setup
1. `cd backend`
2. `cp .env.example .env` (Fill in your credentials)
3. `python -m venv venv`
4. `source venv/bin/activate` # On Windows: `venv\Scripts\activate`
5. `pip install -r requirements.txt`
6. `python run.py`

### Frontend Setup
1. `cd frontend`
2. `cp .env.example .env`
3. `npm install`
4. `npm run dev`

## ☁️ Deployment

### Backend (e.g., Render, Railway, AWS)
- **Environment Variables**: Add all variables from `.env.example` to your platform's dashboard.
- **Port**: The app is configured to run on port 8000 in Docker, or 8001 via `run.py`.
- **Docker**: A `Dockerfile` is provided for containerized deployment.

### Frontend (e.g., Vercel, Netlify)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Environment Variables**: Set `VITE_API_BASE_URL` to your deployed backend URL.

## 📁 Project Structure
- `/backend`: FastAPI service, MongoDB integration, AI services.
- `/frontend`: Vite+React+TypeScript UI.
- `/docs`: Project planning and status tracking.
