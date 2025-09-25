# src/services/mentorship_services.py
from typing import Dict, List, Optional
from src.dao.mentors_dao import MentorsDAO
from src.dao.mentorship_assignment_dao import MentorshipAssignmentsDAO


class MentorshipError(Exception):
    pass


class MentorshipServices:
    def __init__(self):
        self.mentors_dao = MentorsDAO()
        self.assignments_dao = MentorshipAssignmentsDAO()

    # Mentor Management
    def create_mentor(self, alumni_id: int, skills: Optional[str] = None) -> Dict:
        mentor = self.mentors_dao.create_mentor(alumni_id, skills)
        if not mentor:
            raise MentorshipError("Failed to create mentor")
        return mentor

    def get_mentor(self, mentor_id: int) -> Dict:
        mentor = self.mentors_dao.get_mentor_by_id(mentor_id)
        if not mentor:
            raise MentorshipError(f"Mentor with ID {mentor_id} not found")
        return mentor

    def list_mentors(self) -> List[Dict]:
        return self.mentors_dao.list_mentors()

    def update_mentor(self, mentor_id: int, updates: Dict) -> Dict:
        mentor = self.mentors_dao.update_mentor(mentor_id, updates)
        if not mentor:
            raise MentorshipError(f"Failed to update mentor {mentor_id}")
        return mentor

    def delete_mentor(self, mentor_id: int) -> Dict:
        mentor = self.mentors_dao.delete_mentor(mentor_id)
        if not mentor:
            raise MentorshipError(f"Mentor with ID {mentor_id} not found")
        return mentor

    # Mentorship Assignments
    def assign_student(
        self,
        mentor_id: int,
        student_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        # validate mentor
        mentor = self.mentors_dao.get_mentor_by_id(mentor_id)
        if not mentor:
            raise MentorshipError(f"Mentor with ID {mentor_id} not found")

        assignment = self.assignments_dao.assign_student(
            mentor_id, student_id, start_date, end_date
        )
        if not assignment:
            raise MentorshipError("Failed to assign student to mentor")
        return assignment

    def get_assignment(self, assignment_id: int) -> Dict:
        assignment = self.assignments_dao.get_assignment_by_id(assignment_id)
        if not assignment:
            raise MentorshipError(f"Assignment with ID {assignment_id} not found")
        return assignment

    def list_assignments(self) -> List[Dict]:
        return self.assignments_dao.list_assignments()

    def list_students_by_mentor(self, mentor_id: int) -> List[Dict]:
        return self.assignments_dao.list_students_by_mentor(mentor_id)

    def list_mentors_by_student(self, student_id: int) -> List[Dict]:
        return self.assignments_dao.list_mentors_by_student(student_id)

    def update_assignment(self, assignment_id: int, updates: Dict) -> Dict:
        assignment = self.assignments_dao.update_assignment(assignment_id, updates)
        if not assignment:
            raise MentorshipError(f"Failed to update assignment {assignment_id}")
        return assignment

    def delete_assignment(self, assignment_id: int) -> Dict:
        assignment = self.assignments_dao.delete_assignment(assignment_id)
        if not assignment:
            raise MentorshipError(f"Assignment with ID {assignment_id} not found")
        return assignment
