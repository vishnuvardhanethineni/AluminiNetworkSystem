from typing import Optional, List, Dict
from src.config import get_supabase

class MentorshipAssignmentsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def assign_student(self, mentor_id: int, student_id: int, start_date=None, end_date=None) -> Optional[Dict]:
        payload = {
            "mentor_id": mentor_id,
            "student_id": student_id,
            "start_date": start_date,
            "end_date": end_date
        }
        resp = self._sb.table("mentorship_assignments").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_assignment_by_id(self, assignment_id: int) -> Optional[Dict]:
        resp = self._sb.table("mentorship_assignments").select("*").eq("assignment_id", assignment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_assignments(self) -> List[Dict]:
        resp = self._sb.table("mentorship_assignments").select("*").order("created_at", desc=False).execute()
        return resp.data or []

    def list_students_by_mentor(self, mentor_id: int) -> List[Dict]:
        resp = self._sb.table("mentorship_assignments").select("*").eq("mentor_id", mentor_id).execute()
        return resp.data or []

    def list_mentors_by_student(self, student_id: int) -> List[Dict]:
        resp = self._sb.table("mentorship_assignments").select("*").eq("student_id", student_id).execute()
        return resp.data or []

    def update_assignment(self, assignment_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("mentorship_assignments").update(fields).eq("assignment_id", assignment_id).execute()
        resp = self._sb.table("mentorship_assignments").select("*").eq("assignment_id", assignment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_assignment(self, assignment_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("mentorship_assignments").select("*").eq("assignment_id", assignment_id).limit(1).execute()
        assignment = resp_before.data[0] if resp_before.data else None
        if assignment:
            self._sb.table("mentorship_assignments").delete().eq("assignment_id", assignment_id).execute()
        return assignment