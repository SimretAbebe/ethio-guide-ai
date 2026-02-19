# 🚀 Step-by-Step Deployment Guide

Follow these steps to deploy your EthioGuide application. 

## Phase 1: Prepare your Code
Ensure you have pushed your latest local changes to a GitHub repository.

---

## Phase 2: Deploy the Backend (Render)

1.  **Create a New Web Service**:
    - Log in to [Render](https://render.com/).
    - Click **New** -> **Web Service**.
    - Connect your GitHub repository.
2.  **Configure Build Settings**:
    - **Runtime**: `Python 3` (or use the `Dockerfile` if you prefer Docker).
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3.  **Add Environment Variables**:
    - Go to the **Environment** tab.
    - Click **Add Environment Variable** and add:
        - `MONGODB_URI`: (Your MongoDB Atlas connection string)
        - `DATABASE_NAME`: `ethio_guide`
        - `GOOGLE_API_KEY`: (Your Gemini API Key)
        - `ALLOWED_ORIGINS`: `https://your-frontend-domain.vercel.app` (You'll update this after the frontend is deployed).
4.  **Deploy**: Click **Deploy Web Service**. Once finished, copy the provided URL (e.g., `https://ethio-guide-backend.onrender.com`).

---

## Phase 3: Deploy the Frontend (Vercel)

1.  **Create a New Project**:
    - Log in to [Vercel](https://vercel.com/).
    - Click **New Project**.
    - Import your GitHub repository.
2.  **Configure Project Settings**:
    - **Framework Preset**: Vite.
    - **Root Directory**: `frontend`.
3.  **Add Environment Variables**:
    - Expand the **Environment Variables** section.
    - Add:
        - `VITE_API_BASE_URL`: (Paste your Render backend URL **without** a trailing slash).
4.  **Deploy**: Click **Deploy**. Vercel will give you a production URL (e.g., `https://ethio-guide.vercel.app`).

---

## Phase 4: Final Connection (CORS Update)

1.  Go back to your **Render** dashboard.
2.  Select your backend service -> **Environment**.
3.  Update the `ALLOWED_ORIGINS` variable:
    - Replace the placeholder with your actual Vercel URL: `https://ethio-guide.vercel.app`.
4.  Render will automatically redeploy.

---

## Phase 5: Database Access (MongoDB Atlas)

1.  Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2.  Go to **Network Access**.
3.  Click **Add IP Address**.
4.  Select **Allow Access from Anywhere** (`0.0.0.0/0`) for the easiest setup (recommended for starters) OR add the specific IP addresses if your hosting provides them.
