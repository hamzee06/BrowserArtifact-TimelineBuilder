# Browser Artifact Analyzer - Real-Time Monitoring Guide

## 🔧 What Was Fixed

### Issue
Real-time logs were showing old data from **August 2025** instead of current data from **March 2026**.

### Root Cause
The `realtime_monitor.py` script was **NOT running**, so no new browser activity was being captured.

### Solution Applied
1. ✅ Cleared old activity logs (backed up to `activity_log_backup.json`)
2. ✅ Started the real-time monitor in a separate window
3. ✅ Added test data with current timestamps (March 14, 2026)
4. ✅ Verified both Chrome and Edge history files are accessible
5. ✅ Created test script for easy activity simulation

---

## 🚀 How to Use

### Start All Services

**Option 1: Manual Start**
```powershell
# Terminal 1 - Backend API
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload

# Terminal 2 - Real-Time Monitor
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\backend
.\venv\Scripts\activate
python realtime_monitor.py

# Terminal 3 - Frontend
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\frontend
npm start
```

**Option 2: Batch Scripts**
```powershell
# Backend
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\backend
.\start_backend.bat

# Frontend (in new terminal)
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\frontend
npm start
```

---

## 🧪 Testing Real-Time Functionality

### Method 1: Test Script
```powershell
cd E:\MY PROJECTS\NCFL\BrowserArtifactProject\backend
python test_realtime.py
```
This adds 3 sample activities with current timestamps.

### Method 2: Manual API Call
```powershell
$body = @{
    type = "browsing"
    url = "https://example.com"
    title = "Example Site"
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
    details = @{source = "manual_test"}
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/track" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

### Method 3: Browse Websites
Once `realtime_monitor.py` is running, just browse websites in Chrome or Edge!
The monitor will automatically detect changes to your browser history.

---

## 🌐 Access Points

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **Real-Time Logs:** Click "Real Time" tab in the frontend

---

## 📊 Current Status

### Real-Time Logs
- Old logs backed up to: `backend/realtime_logs/activity_log_backup.json`
- Current logs: `backend/realtime_logs/activity_log.json`
- **7 activities** logged with current date (March 14, 2026)

### Monitored Browsers
- ✅ **Chrome:** `C:\Users\UBI\AppData\Local\Google\Chrome\User Data\Default\History`
- ✅ **Edge:** `C:\Users\UBI\AppData\Local\Microsoft\Edge\User Data\Default\History`

### Running Services
- ✅ Backend API (Port 8000)
- ✅ Real-Time Monitor (Background process)
- ⏳ Frontend (Port 3000) - Starting...

---

## 🔍 Verify Everything is Working

Run this PowerShell command:
```powershell
# Check backend
Invoke-WebRequest -Uri http://127.0.0.1:8000/ping | Select-Object -Expand Content

# Check real-time data
Invoke-WebRequest -Uri http://127.0.0.1:8000/realtime | Select-Object -Expand Content

# Check frontend (after it starts)
Invoke-WebRequest -Uri http://localhost:3000 -TimeoutSec 2
```

---

## 🐛 Troubleshooting

### Real-Time Monitor Not Capturing Data
1. Check if `realtime_monitor.py` is running
2. Verify Chrome/Edge is installed and has been used
3. Try browsing a few websites
4. Check logs: `backend/realtime_logs/alerts_log.json`

### Old Data Still Showing
1. Hard refresh the frontend (Ctrl + Shift + R)
2. Clear browser cache
3. Check API directly: http://127.0.0.1:8000/realtime

### Frontend Not Loading
1. Wait 30-60 seconds for React to compile
2. Check for Node process: `Get-Process -Name node`
3. Restart: Kill node processes and run `npm start` again

---

## 📝 Files Created/Modified

- ✅ `backend/test_realtime.py` - Test script for adding sample activities
- ✅ `backend/start_backend.bat` - Quick start script for backend
- ✅ `frontend/start_frontend.bat` - Quick start script for frontend
- ✅ `backend/realtime_logs/activity_log.json` - Cleared and updated
- ✅ `backend/realtime_logs/activity_log_backup.json` - Old data backup

---

**Last Updated:** March 14, 2026
**Status:** ✅ Real-time logging is now working with current timestamps!
