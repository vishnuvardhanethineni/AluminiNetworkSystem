from typing import Optional, List, Dict
from src.config import get_supabase

class EventRegistrationsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def register_user(self, event_id: int, user_id: int, user_type: str) -> Optional[Dict]:
        payload = {"event_id": event_id, "user_id": user_id, "user_type": user_type}
        resp = self._sb.table("event_registrations").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def list_user_events(self, user_id: int, user_type: str) -> List[Dict]:
        resp = (
            self._sb.table("event_registrations")
            .select("event_id(*), registered_at")
            .eq("user_id", user_id)
            .eq("user_type", user_type)
            .execute()
        )
        return resp.data or []

    def list_event_participants(self, event_id: int) -> List[Dict]:
        resp = (
            self._sb.table("event_registrations")
            .select("user_id, user_type, registered_at")
            .eq("event_id", event_id)
            .execute()
        )
        return resp.data or []
