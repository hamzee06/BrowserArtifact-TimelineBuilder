# models/history_model.py
from pydantic import BaseModel

class HistoryItem(BaseModel):
    url: str
    title: str
    last_visit_time: str
