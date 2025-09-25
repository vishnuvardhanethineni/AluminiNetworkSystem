from typing import Optional, List, Dict
from src.config import get_supabase

class EventsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_event(self, payload: Dict) -> Optional[Dict]:
        resp = self._sb.table("events").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_event_by_id(self, event_id: int) -> Optional[Dict]:
        resp = self._sb.table("events").select("*").eq("event_id", event_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_events(self) -> List[Dict]:
        resp = self._sb.table("events").select("*").order("event_date", desc=False).execute()
        return resp.data or []

    def update_event(self, event_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("events").update(fields).eq("event_id", event_id).execute()
        resp = self._sb.table("events").select("*").eq("event_id", event_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_event(self, event_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("events").select("*").eq("event_id", event_id).limit(1).execute()
        event = resp_before.data[0] if resp_before.data else None
        if event:
            self._sb.table("events").delete().eq("event_id", event_id).execute()
        return event
