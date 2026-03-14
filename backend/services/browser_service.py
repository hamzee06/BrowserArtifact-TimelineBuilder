# services/browser_service.py
import sqlite3
import json
import os
import tempfile
from datetime import datetime, timedelta
from typing import List, Dict, Any

# ---------- Helpers ----------

def convert_chrome_time(chrome_time):
    """
    Convert Chrome time (microseconds since 1601-01-01) to ISO string.
    If value is None or not numeric, return None.
    """
    try:
        epoch_start = datetime(1601, 1, 1)
        # Chrome stores microseconds
        dt = epoch_start + timedelta(microseconds=int(chrome_time))
        return dt.isoformat()
    except Exception:
        return None

# ---------- Extractors for uploaded SQLite DBs ----------

def extract_history(db_path: str) -> List[Dict[str, Any]]:
    items = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url, title, last_visit_time FROM urls
            ORDER BY last_visit_time DESC LIMIT 20
        """)
        rows = cursor.fetchall()
        conn.close()
        for url, title, last_visit in rows:
            items.append({
                "url": url,
                "title": title,
                "last_visit_time": convert_chrome_time(last_visit)
            })
    except Exception as e:
        print("extract_history error:", e)
    return items

def extract_logins(db_path: str) -> List[Dict[str, Any]]:
    items = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        rows = cursor.fetchall()
        conn.close()
        for origin, user, pwd in rows:
            items.append({
                "origin_url": origin,
                "username": user,
                "password": "[ENCRYPTED]"
            })
    except Exception as e:
        print("extract_logins error:", e)
    return items

def extract_cookies(db_path: str) -> List[Dict[str, Any]]:
    items = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, value, expires_utc FROM cookies")
        rows = cursor.fetchall()
        conn.close()
        for host, name, value, expires in rows:
            items.append({
                "host_key": host,
                "name": name,
                "value": value,
                "expires_utc": convert_chrome_time(expires)
            })
    except Exception as e:
        print("extract_cookies error:", e)
    return items

# ---------- Realtime log writer / reader ----------

_LOG_DIR = "realtime_logs"
_LOG_FILE = os.path.join(_LOG_DIR, "activity_log.json")

def _ensure_logfile():
    os.makedirs(_LOG_DIR, exist_ok=True)
    if not os.path.exists(_LOG_FILE):
        with open(_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def read_realtime_activity() -> List[Dict[str, Any]]:
    """
    Returns the list of activity entries. If file missing or corrupt, returns [].
    """
    _ensure_logfile()
    try:
        with open(_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except json.JSONDecodeError:
        print("read_realtime_activity: JSON decode error, returning empty list.")
    except Exception as e:
        print("read_realtime_activity error:", e)
    return []

def save_realtime_activity(activity_data: Dict[str, Any]):
    """
    Append activity_data to the JSON log atomically.
    Normalizes a few common fields.
    """
    _ensure_logfile()

    # Normalize / build entry
    entry = {
        "timestamp": activity_data.get("timestamp") or activity_data.get("start_time") or datetime.utcnow().isoformat(),
        "type": activity_data.get("type") or activity_data.get("event") or "unknown",
        "url": activity_data.get("url"),
        "title": activity_data.get("title"),
        "details": activity_data.get("details") or {},
    }

    # Read-modify-write with a safe temp file and os.replace to reduce corruption risk
    try:
        with open(_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            except json.JSONDecodeError:
                logs = []
    except FileNotFoundError:
        logs = []

    logs.append(entry)

    # atomic write to temp file then replace
    fd, tmp_path = tempfile.mkstemp(prefix="activity_", suffix=".json", dir=_LOG_DIR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            json.dump(logs, tmp, indent=4)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, _LOG_FILE)
    except Exception as e:
        print("save_realtime_activity write error:", e)
        # cleanup temp if exists
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

    # Friendly console feedback for debugging
    print("Saved activity entry:", entry)
