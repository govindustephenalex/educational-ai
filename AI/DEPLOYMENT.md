# Deployment Instructions

## Local Deployment

1.  **Prerequisites**:
    - Python 3.9+
    - Node.js (optional, if you want to serve frontend via a server, but opening HTML works too)

2.  **Backend Setup**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    - Create a `.env` file in `backend/app/core/` (or root of backend).
    - Add: `OPENAI_API_KEY=your_api_key_here`

4.  **Run Backend**:
    ```bash
    uvicorn app.main:app --reload
    ```
    API will mock responses if no API key is provided, or fail gracefully.

5.  **Run Frontend**:
    - Simply double-click `frontend/index.html` to open it in your browser.
    - Or using Python: `python -m http.server 3000` inside frontend folder.

## Cloud Deployment (Render / Railway)

1.  **Backend**:
    - Push code to GitHub.
    - Connect repo to Render/Railway.
    - Set Build Command: `pip install -r backend/requirements.txt`
    - Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
    - Add `OPENAI_API_KEY` in Environment Variables.

2.  **Frontend**:
    - Host on Vercel or Netlify.
    - Update `script.js` fetch URL to point to your deployed Backend URL instead of `localhost:8000`.
