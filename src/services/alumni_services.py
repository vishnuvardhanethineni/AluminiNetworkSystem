# src/services/alumni_service.py
from typing import Dict, List, Optional
from src.dao.alumni_dao import AlumniDAO
from src.dao.event_registrations import EventRegistrationsDAO
from src.services.event_services import EventService, EventError


class AlumniError(Exception):
    """Custom exception for Alumni service errors."""
    pass


class AlumniService:
    def __init__(self):
        self.alumni_dao = AlumniDAO()
        self.event_service = EventService()
        self.reg_dao = EventRegistrationsDAO()

    # Alumni CRUD
    def add_alumni(self, payload: Dict) -> Dict:
        required_fields = ["name", "email", "industry", "graduation_year", "location"]
        for field in required_fields:
            if field not in payload or not payload[field]:
                raise AlumniError(f"Missing required field: {field}")

        # Check if email already exists
        existing = self.alumni_dao.search_alumni("email", payload["email"])
        if existing:
            raise AlumniError("An alumni with this email already exists")

        return self.alumni_dao.create_alumni(payload)

    def update_alumni(self, alumni_id: int, updates: Dict) -> Dict:
        alumni = self.alumni_dao.get_alumni_by_id(alumni_id)
        if not alumni:
            raise AlumniError(f"Alumni with ID {alumni_id} not found")
        return self.alumni_dao.update_alumni(alumni_id, updates)

    def get_alumni(self, alumni_id: int) -> Dict:
        alumni = self.alumni_dao.get_alumni_by_id(alumni_id)
        if not alumni:
            raise AlumniError(f"Alumni with ID {alumni_id} not found")
        return alumni

    def list_alumni(self, filters: Optional[Dict] = None) -> List[Dict]:
        return self.alumni_dao.list_alumni(filters)

    def search_alumni(self, field: str, value) -> List[Dict]:
        results = self.alumni_dao.search_alumni(field, value)
        if not results:
            raise AlumniError(f"No alumni found with {field} = {value}")
        return results

    def remove_alumni(self, alumni_id: int) -> Dict:
        alumni = self.alumni_dao.get_alumni_by_id(alumni_id)
        if not alumni:
            raise AlumniError(f"Alumni with ID {alumni_id} not found")
        return self.alumni_dao.delete_alumni(alumni_id)

    # Event-related functions
    def search_events(self, filters: Dict = None) -> List[Dict]:
        try:
            return self.event_service.list_events(filters)
        except EventError as e:
            raise AlumniError(f"Event search failed: {e}")

    def join_event(self, alumni_id: int, event_id: int) -> Dict:
        try:
            # Ensure event exists
            self.event_service.get_event(event_id)

            registration = self.reg_dao.register_user(event_id, alumni_id, "alumni")
            if not registration:
                raise AlumniError(f"Alumni {alumni_id} could not join event {event_id}.")
            return registration
        except EventError as e:
            raise AlumniError(f"Join event failed: {e}")

    def list_my_events(self, alumni_id: int) -> List[Dict]:
        try:
            return self.reg_dao.list_user_events(alumni_id, "alumni") or []
        except Exception as e:
            raise AlumniError(f"Could not fetch events for alumni {alumni_id}: {e}")
