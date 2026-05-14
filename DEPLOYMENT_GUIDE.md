# 🚀 Deployment Guide - Nutrisense Diet Recommendation System

This guide covers deploying to **Streamlit Cloud** (Frontend) and **Render** (Backend).

---

## 📋 Deployment Overview

| Component | Platform | Time to Deploy | Cost |
|-----------|----------|----------------|------|
| **Frontend (Streamlit)** | Streamlit Cloud | ~5 minutes | Free |
| **Backend (FastAPI)** | Render | ~5 minutes | Free (with limitations) |
| **Database** | Cloud (optional) | N/A | Depends |

---

## 🎯 Part 1: Deploy Backend to Render

### Step 1: Prepare the Backend

1. Ensure all files are in your Git repository:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   ```

2. The repository should have this structure:
   ```
   ├── FastAPI_Backend/
   │   ├── main.py
   │   ├── model.py
   │   ├── requirements.txt
   │   └── Dockerfile
   ├── Data/
   │   └── dataset.csv
   └── docker-compose.yml
   ```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up (free account)
3. Connect your GitHub account

### Step 3: Deploy Backend Service

1. Click **"New +"** → **"Web Service"**
2. Select your repository
3. Configure:
   - **Name:** `nutrisense-backend`
   - **Environment:** `Docker`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Build Command:** (Leave empty, uses Dockerfile)
   - **Start Command:** (Leave empty, uses Dockerfile CMD)
4. Click **"Create Web Service"**
5. **Wait 5-10 minutes** for build completion
6. Copy the deployed URL: `https://nutrisense-backend-xxxx.onrender.com`

### Step 4: Set Up Backend Dockerfile (if needed)

Create `FastAPI_Backend/Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY FastAPI_Backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY Data /app/Data
COPY FastAPI_Backend /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 🎯 Part 2: Deploy Frontend to Streamlit Cloud

### Step 1: Prepare Frontend Repository

Your Streamlit frontend must be in a public GitHub repository with:
```
Streamlit_Frontend/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml (for secrets)
├── Hello.py (main page)
├── pages/
│   ├── 1_Diet_Recommendation.py
│   └── 2_Custom_Food_Recommendation.py
├── ImageFinder/
├── Generate_Recommendations.py
└── requirements.txt
```

### Step 2: Create Streamlit Cloud Account

1. Go to https://streamlit.io/cloud
2. Sign up with GitHub
3. Authorize Streamlit to access your repositories

### Step 3: Deploy Frontend

1. Click **"New app"**
2. Select your repository
3. Configure:
   - **Repository:** Select your repo
   - **Branch:** `main`
   - **Main file path:** `Streamlit_Frontend/Hello.py`
4. Click **"Deploy"**
5. **Wait 2-5 minutes** for deployment

### Step 4: Configure Backend URL in Secrets

After deployment:

1. Click on **"Settings"** (gear icon, top right)
2. Go to **"Secrets"** tab
3. Add this to the editor (replace with your Render URL):
   ```
   backend_url = "https://nutrisense-backend-xxxx.onrender.com"
   ```
4. Click **"Save"**
5. Streamlit will redeploy automatically

### Step 5: Update Frontend Code to Use Backend URL

The frontend should reference the backend URL from secrets:

```python
import streamlit as st

# Get backend URL from secrets
BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8080")

# Use in API calls:
# response = requests.post(f"{BACKEND_URL}/predict", json=data)
```

---

## 🔄 Connecting Frontend to Backend

### Update `Generate_Recommendations.py`

```python
import requests
import streamlit as st
import json

# Get backend URL
BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8080")

class Generator:
    def __init__(self, nutrition_input, ingredients=[], params=None):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params or {'n_neighbors': 5, 'return_distance': False}
    
    def generate(self):
        """Call FastAPI backend"""
        try:
            payload = {
                "nutrition_input": self.nutrition_input,
                "ingredients": self.ingredients,
                "params": self.params
            }
            
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response
            else:
                st.error(f"Backend error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}")
            return None
```

---

## 🧪 Testing Your Deployment

### Local Testing (Before Deployment)

1. Start backend:
   ```bash
   cd FastAPI_Backend
   uvicorn main:app --reload --port 8080
   ```

2. In another terminal, start frontend:
   ```bash
   cd Streamlit_Frontend
   streamlit run Hello.py
   ```

3. Test recommendations

### Production Testing

1. Access Streamlit Cloud app URL
2. Test each page (Diet Recommendation, Custom Food)
3. Check Network tab in browser DevTools for backend requests
4. Monitor backend logs on Render dashboard

---

## 📊 Monitoring & Logs

### View Render Backend Logs
- Go to https://dashboard.render.com
- Click your service
- View "Logs" tab in real-time

### View Streamlit Cloud Logs
- Go to https://share.streamlit.io
- Click your app
- View "Logs" in the menu

### Common Issues

| Issue | Solution |
|-------|----------|
| "Failed to connect to backend" | Update `backend_url` in Streamlit Secrets |
| 502 Bad Gateway | Backend may be restarting (Render free tier hibernates) |
| CORS errors | Add CORS middleware to FastAPI backend |
| Slow response | Render free tier may be underpowered; upgrade if needed |

---

## 💾 Data Management

### Render Free Tier Limitations
- **Hibernates after 15 minutes of inactivity**
- **Shared resources** (slower)
- **No persistent storage** (reset on restart)

### Upgrade Options
1. **Render Paid Tier** (~$5/month): Always-on service
2. **Railway**: More reliable for ML models
3. **AWS/DigitalOcean**: Enterprise solution

---

## 🔐 Security Best Practices

1. **Never commit secrets** to GitHub
2. **Use Streamlit Secrets** for backend URL
3. **Set up CORS** properly in FastAPI:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Restrict in production
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Enable HTTPS** (both platforms provide this by default)
5. **Validate all inputs** on backend

---

## 📝 Summary Checklist

- [ ] Backend code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Get Render backend URL
- [ ] Frontend code ready with `.streamlit/` folder
- [ ] Frontend deployed on Streamlit Cloud
- [ ] Update Streamlit Secrets with backend URL
- [ ] Test frontend-backend connection
- [ ] Monitor logs and performance
- [ ] (Optional) Upgrade from free tier

---

## 📞 Support & Resources

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Render Docs**: https://render.com/docs
- **FastAPI CORS**: https://fastapi.tiangolo.com/tutorial/cors/
- **Troubleshooting**: Check logs on both platforms

---

**🎉 Your application is now live on the cloud!**
