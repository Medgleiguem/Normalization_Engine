# Deployment Guide

This guide explains how to deploy the Normalization Engine application. We recommend using **Render.com** as it supports both Python (Flask) and Node.js (React) applications in a single unified platform.

## Prerequisites

1.  **GitHub Account**: Your project code must be pushed to a GitHub repository.
2.  **Render Account**: Sign up at [render.com](https://render.com).

## Part 1: Repository Setup

1.  **Important**: Ensure your `node_modules` folders are NOT in GitHub.
    - We have already updated your `.gitignore` files.
    - If you see `node_modules` in your GitHub repo, run this in your terminal:
      ```bash
      git rm -r --cached frontend/node_modules backend/node_modules
      git commit -m "Remove node_modules"
      git push
      ```

2.  **Project Structure**:
    Your project is set up as a monorepo (both frontend and backend in one repo).
    - `frontend/`: React application
    - `backend/`: Flask application

## Part 2: Deploying the Backend (Flask)

1.  **New Web Service**:
    - Go to Render Dashboard -> New -> Web Service.
    - Connect your GitHub repository.

2.  **Configuration**:
    - **Name**: `normalization-engine-backend`
    - **Root Directory**: `backend` (Important!)
    - **Runtime**: Python 3
    - **Note**: A `.python-version` file is included in the project root to ensure Render uses Python 3.11, which is required for dependencies like pandas.
    - **Build Command**: `pip install -r requirements.txt && npm install`
      _(Note: We add npm install because your backend uses a Node.js script for report generation)_
    - **Start Command**: `gunicorn run:app`
    - **Environment Variables**:
      - `FLASK_ENV`: `production`
      - `PORT`: `5000`

## Part 3: Deploying the Frontend (React)

1.  **New Static Site**:
    - Go to Render Dashboard -> New -> Static Site.
    - Connect the **same** GitHub repository.

2.  **Configuration**:
    - **Name**: `normalization-engine-frontend`
    - **Root Directory**: `frontend` (Important!)
    - **Build Command**: `npm install && npm run build`
    - **Publish Directory**: `dist` (or `build` if using Create React App)
    - **Environment Variables**:
      - `VITE_API_URL`: `https://normalization-engine-backend.onrender.com/api`
        _(Replace this URL with the actual URL of your deployed backend from Part 2. Ensure you add `/api` at the end)_

## Part 4: Final Steps

1.  **Update Backend CORS**:
    - Once your frontend is deployed, you might need to update your Flask CORS settings to allow requests from your new frontend domain (`https://normalization-engine-frontend.onrender.com`).
    - In `backend/app/__init__.py` or where `CORS(app)` is initialized, ensure it accepts the new origin.

2.  **Test**:
    - Open your frontend URL.
    - Try uploading a file to verify the connection to the backend works.

## Troubleshooting

- **500 Errors**: Check the "Logs" tab in Render for your backend service.
- **CORS Errors**: Check browser console. Ensure backend allows the frontend domain.
- **Build Fails**: Check if `package-lock.json` or `requirements.txt` is missing.
