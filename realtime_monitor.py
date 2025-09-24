"""
Enhanced Realtime Monitor for Windows:
- Monitors Chrome/Edge History SQLite files (using watchdog)
- Monitors critical registry keys (homepage, extensions, proxy, search engine)
- Sends desktop popups, email alerts, and logs all events in JSON
"""

import os
import sys
import time
import shutil
import sqlite3
import threading
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add project root to sys.path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from services.browser_service import save_realtime_activity
from notifier import show_popup, log_alert, send_email_alert  # Import notification utilities

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import winreg
    import win32api
    import win32con
    if not hasattr(win32con, "REG_NOTIFY_CHANGE_LAST_SET"):
        win32con.REG_NOTIFY_CHANGE_LAST_SET = 0x00000004
except Exception as e:
    print("pywin32/winreg import error (registry features disabled):", e)
    winreg = None

# Paths for Chrome and Edge History DB
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
CHROME_HISTORY = os.path.join(LOCALAPPDATA, r"Google\Chrome\User Data\Default\History")
EDGE_HISTORY = os.path.join(LOCALAPPDATA, r"Microsoft\Edge\User Data\Default\History")
HISTORY_CANDIDATES = [CHROME_HISTORY, EDGE_HISTORY]

# Critical registry keys to watch
REG_KEYS_TO_WATCH = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"),
    (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")  # Proxy settings
] if winreg else []


def alert_change(message):
    """Unified alert function for logging, popup, and email notification."""
    log_alert(message)
    show_popup(message)
    send_email_alert("Critical Change Detected", message)


def read_latest_from_history(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url, title, last_visit_time
            FROM urls
            ORDER BY last_visit_time DESC LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            url, title, last_visit_time = row
            epoch_start = datetime(1601, 1, 1, tzinfo=timezone.utc)
            dt_utc = epoch_start + timedelta(microseconds=int(last_visit_time))
            dt_local = dt_utc.astimezone()  # convert to system local timezone
            return {
                "type": "history",
                "url": url,
                "title": title,
                "timestamp": dt_local.isoformat()
            }
    except Exception as e:
        print("read_latest_from_history error:", e)
    return None


class HistoryEventHandler(FileSystemEventHandler):
    def __init__(self, original_path):
        super().__init__()
        self.original_path = original_path

    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path).lower() == "history":
            print(f"[watcher] Detected change to {event.src_path}")
            try:
                tmp = os.path.join(os.path.dirname(self.original_path), f"history_copy_{int(time.time())}.db")
                shutil.copy2(self.original_path, tmp)
                data = read_latest_from_history(tmp)
                os.remove(tmp)
                if data:
                    save_realtime_activity({
                        "type": "history",
                        "url": data.get("url"),
                        "title": data.get("title"),
                        "timestamp": data.get("timestamp"),
                        "details": {"source": self.original_path}
                    })
                    alert_change(f"New browsing activity detected:\n{data.get('title')} - {data.get('url')}")
                    print("[watcher] Saved history entry:", data.get("url"))
            except Exception as e:
                print("HistoryEventHandler error:", e)


def start_history_watchers():
    observer = Observer()
    found_any = False
    for candidate in HISTORY_CANDIDATES:
        if os.path.exists(candidate):
            handler = HistoryEventHandler(candidate)
            observer.schedule(handler, path=os.path.dirname(candidate), recursive=False)
            print("[monitor] Watching history file at:", candidate)
            found_any = True
    if not found_any:
        print("[monitor] No History files found.")
        return None
    observer.start()
    return observer


def registry_watcher_thread(hive, subkey):
    try:
        print(f"[registry] Watching HKCU\\{subkey}")
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        while True:
            win32api.RegNotifyChangeKeyValue(key, True, win32con.REG_NOTIFY_CHANGE_LAST_SET, None, False)
            try:
                info = {}
                i = 0
                while True:
                    try:
                        val = winreg.EnumValue(key, i)
                        info[val[0]] = val[1]
                        i += 1
                    except OSError:
                        break
                message = f"Registry change detected in {subkey}:\n{info}"
                save_realtime_activity({
                    "type": "registry",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "details": {"subkey": subkey, "values": info}
                })
                alert_change(message)
                print(f"[registry] Change detected and logged for {subkey}")
            except Exception as e:
                print("Registry read error:", e)
    except Exception as e:
        print("registry_watcher_thread error:", e)


def start_registry_watchers():
    if not winreg:
        print("[registry] pywin32 not available; skipping registry watchers.")
        return []
    threads = []
    for hive, subkey in REG_KEYS_TO_WATCH:
        t = threading.Thread(target=registry_watcher_thread, args=(hive, subkey), daemon=True)
        t.start()
        threads.append(t)
    return threads


def main():
    print("[monitor] Starting enhanced realtime monitor...")
    observer = start_history_watchers()
    start_registry_watchers()
    if observer is None:
        print("[monitor] No history watcher started. Exiting in 10s.")
        time.sleep(10)
        return
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[monitor] Stopping monitor...")
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
