from typing import Dict, List, Optional
from src.dao.students_dao import StudentsDAO
from src.dao.event_registrations import EventRegistrationsDAO
from src.services.event_services import EventService, EventError
from src.services.mentorship_services import MentorshipServices, MentorshipError


class StudentError(Exception):
    """Custom exception for Student service errors."""
    pass


class StudentService:
    def __init__(self):
        self.dao = StudentsDAO()
        self.event_service = EventService()
        self.reg_dao = EventRegistrationsDAO()
        self.mentorship_service = MentorshipServices()  # Add mentorship services

    # --- Student CRUD ---
    def create_student(self, name: str, email: str, course: str = None, year: int = None) -> Dict:
        existing = self.dao.get_student_by_email(email)
        if existing:
            raise StudentError(f"Student with email {email} already exists.")
        return self.dao.create_student(name, email, course, year)

    def get_student(self, student_id: int) -> Optional[Dict]:
        return self.dao.get_student_by_id(student_id)

    def list_students(self, filters: Dict = None) -> List[Dict]:
        students = self.dao.list_students()
        if filters:
            filtered = []
            for s in students:
                match = True
                for k, v in filters.items():
                    if str(s.get(k)).lower() != str(v).lower():
                        match = False
                        break
                if match:
                    filtered.append(s)
            return filtered
        return students

    def update_student(self, student_id: int, fields: Dict) -> Optional[Dict]:
        student = self.dao.get_student_by_id(student_id)
        if not student:
            raise StudentError(f"Student ID {student_id} does not exist.")
        return self.dao.update_student(student_id, fields)

    def delete_student(self, student_id: int) -> Optional[Dict]:
        student = self.dao.get_student_by_id(student_id)
        if not student:
            raise StudentError(f"Student ID {student_id} does not exist.")
        return self.dao.delete_student(student_id)

    # --- Event-related functions ---
    def search_events(self, filters: Dict = None) -> List[Dict]:
        try:
            return self.event_service.list_events(filters)
        except EventError as e:
            raise StudentError(f"Event search failed: {e}")

    def join_event(self, student_id: int, event_id: int) -> Dict:
        try:
            # Ensure event exists
            self.event_service.get_event(event_id)
            registration = self.reg_dao.register_user(event_id, student_id, "student")
            if not registration:
                raise StudentError(f"Student {student_id} could not join event {event_id}.")
            return registration
        except EventError as e:
            raise StudentError(f"Join event failed: {e}")

    def list_my_events(self, student_id: int) -> List[Dict]:
        try:
            return self.reg_dao.list_user_events(student_id, "student") or []
        except Exception as e:
            raise StudentError(f"Could not fetch events for student {student_id}: {e}")

    # --- Mentorship-related functions ---
    def list_all_mentors(self) -> List[Dict]:
        try:
            return self.mentorship_service.list_mentors()
        except MentorshipError as e:
            raise StudentError(f"Could not list mentors: {e}")

    def join_mentorship(
        self,
        student_id: int,
        mentor_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        # Validate student
        student = self.dao.get_student_by_id(student_id)
        if not student:
            raise StudentError(f"Cannot join mentorship: Student with ID {student_id} does not exist.")

        # Validate mentor
        try:
            mentor = self.mentorship_service.get_mentor(mentor_id)
        except MentorshipError:
            raise StudentError(f"Cannot join mentorship: Mentor with ID {mentor_id} does not exist.")

        # Assign student to mentor
        try:
            assignment = self.mentorship_service.assign_student(mentor_id, student_id, start_date, end_date)
            return assignment
        except MentorshipError as e:
            raise StudentError(f"Failed to join mentorship: {e}")

    def list_my_mentors(self, student_id: int) -> List[Dict]:
        try:
            return self.mentorship_service.list_mentors_by_student(student_id)
        except MentorshipError as e:
            raise StudentError(f"Cannot list mentors: {e}")
