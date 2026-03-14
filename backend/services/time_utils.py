from datetime import datetime, timedelta

def convert_chrome_time(chrome_time: int) -> str:
    """
    Convert Chrome/Webkit timestamp (microseconds since 1601) to readable datetime string.
    """
    if chrome_time == 0:
        return ""
    epoch_start = datetime(1601, 1, 1)
    converted_time = epoch_start + timedelta(microseconds=chrome_time)
    return converted_time.strftime('%Y-%m-%d %H:%M:%S')
