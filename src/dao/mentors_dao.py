from typing import Optional, List, Dict
from src.config import get_supabase

class MentorsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_mentor(self, alumni_id: int, skills: str = None) -> Optional[Dict]:
        payload = {"alumni_id": alumni_id, "skills": skills}
        resp = self._sb.table("mentors").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_mentor_by_id(self, mentor_id: int) -> Optional[Dict]:
        resp = self._sb.table("mentors").select("*").eq("mentor_id", mentor_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_mentors(self) -> List[Dict]:
        resp = self._sb.table("mentors").select("*").order("mentor_id", desc=False).execute()
        return resp.data or []

    def update_mentor(self, mentor_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("mentors").update(fields).eq("mentor_id", mentor_id).execute()
        resp = self._sb.table("mentors").select("*").eq("mentor_id", mentor_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_mentor(self, mentor_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("mentors").select("*").eq("mentor_id", mentor_id).limit(1).execute()
        mentor = resp_before.data[0] if resp_before.data else None
        if mentor:
            self._sb.table("mentors").delete().eq("mentor_id", mentor_id).execute()
        return mentor
