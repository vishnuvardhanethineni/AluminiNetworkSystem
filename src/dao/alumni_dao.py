from src.config import get_supabase
from typing import Dict, List, Optional

class AlumniDAO:
    def __init__(self):
        self._sb = get_supabase()

    # Create a new alumni record
    def create_alumni(self, payload: Dict) -> Optional[Dict]:
        resp = self._sb.table("alumni").insert(payload).execute()
        return resp.data[0] if resp.data else None

    # Update any field(s) of an alumni
    def update_alumni(self, alumni_id: int, updates: Dict) -> Optional[Dict]:
        resp = self._sb.table("alumni").update(updates).eq("alumni_id", alumni_id).execute()
        return resp.data[0] if resp.data else None

    # Get alumni by ID
    def get_alumni_by_id(self, alumni_id: int) -> Optional[Dict]:
        resp = self._sb.table("alumni").select("*").eq("alumni_id", alumni_id).execute()
        return resp.data[0] if resp.data else None

    # List all alumni (optionally with filters)
    def list_alumni(self, filters: Dict = None) -> List[Dict]:
        query = self._sb.table("alumni").select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        resp = query.execute()
        return resp.data if resp.data else []

    # Search alumni by any single field
    def search_alumni(self, field: str, value) -> List[Dict]:
        resp = self._sb.table("alumni").select("*").eq(field, value).execute()
        return resp.data if resp.data else []

    # Delete an alumni by ID
    def delete_alumni(self, alumni_id: int) -> Optional[Dict]:
        resp = self._sb.table("alumni").delete().eq("alumni_id", alumni_id).execute()
        return resp.data[0] if resp.data else None
