from fastapi import APIRouter, UploadFile, File, Request
from services import browser_service
import os
import shutil
import json

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Artifact Upload Endpoints ----------

@router.post("/history")
async def history(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    data = browser_service.extract_history(file_path)
    return data

@router.post("/cookies")
async def cookies(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    data = browser_service.extract_cookies(file_path)
    return data

@router.post("/logins")
async def logins(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    data = browser_service.extract_logins(file_path)
    return data

# ---------- Real-Time Tracking Endpoints ----------

@router.post("/track")
async def track_activity(request: Request):
    try:
        activity_data = await request.json()
        print("Received activity:", activity_data)
        browser_service.save_realtime_activity(activity_data)
        return {"status": "success", "message": "Activity recorded"}
    except Exception as e:
        print("Error saving activity:", e)
        return {"status": "error", "message": str(e)}

@router.get("/realtime")
def get_realtime_activity():
    file_path = "realtime_logs/activity_log.json"
    if not os.path.exists(file_path):
        return {"status": "empty", "data": []}
    with open(file_path, "r") as f:
        data = json.load(f)
    return {"status": "ok", "data": data}
