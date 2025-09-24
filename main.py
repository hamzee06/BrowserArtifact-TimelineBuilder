# main.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from services.browser_service import (
    extract_history,
    extract_logins,
    extract_cookies,
    save_realtime_activity,
    read_realtime_activity,
)
import os
import shutil

app = FastAPI()

# Enable CORS for development (allow any origin). Lock this down in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Browser Artifact Analyzer"}

@app.get("/ping")
def ping():
    return {"message": "Backend is live"}

# --- Artifact upload endpoints ---

@app.post("/history")
async def upload_history(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        return extract_history(file_path)
    except Exception as e:
        return {"error": str(e)}

@app.post("/logins")
async def upload_logins(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        return extract_logins(file_path)
    except Exception as e:
        return {"error": str(e)}

@app.post("/cookies")
async def upload_cookies(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        return extract_cookies(file_path)
    except Exception as e:
        return {"error": str(e)}

# --- Realtime tracking endpoints ---

@app.post("/track")
async def track_activity(request: Request):
    """
    Endpoint used by any client (extension, monitor) to push activity.
    Saves using browser_service.save_realtime_activity.
    """
    try:
        activity_data = await request.json()
        print("Received /track payload:", activity_data)
        save_realtime_activity(activity_data)
        return {"status": "success", "message": "Activity recorded"}
    except Exception as e:
        print("Error in /track:", e)
        return {"status": "error", "message": str(e)}

@app.get("/realtime")
def get_realtime():
    """
    Return stored realtime logs in a standard format:
    { "status": "ok", "data": [ ... ] }
    """
    try:
        data = read_realtime_activity()
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
