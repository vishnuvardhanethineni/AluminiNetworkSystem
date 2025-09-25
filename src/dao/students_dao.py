# src/dao/students_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class StudentsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_student(self, name: str, email: str, course: str = None, year: int = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "course": course, "year": year}
        resp = self._sb.table("students").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        resp = self._sb.table("students").select("*").eq("student_id", student_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_student_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("students").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_students(self) -> List[Dict]:
        resp = self._sb.table("students").select("*").order("student_id", desc=False).execute()
        return resp.data or []

    def update_student(self, student_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("students").update(fields).eq("student_id", student_id).execute()
        resp = self._sb.table("students").select("*").eq("student_id", student_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_student(self, student_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("students").select("*").eq("student_id", student_id).limit(1).execute()
        student = resp_before.data[0] if resp_before.data else None
        if student:
            self._sb.table("students").delete().eq("student_id", student_id).execute()
        return student
