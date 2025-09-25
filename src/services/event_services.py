# src/services/event_service.py
from typing import Optional, List, Dict
from src.dao.events_dao import EventsDAO

class EventError(Exception):
    """Custom exception for Event service errors."""
    pass

class EventService:
    def __init__(self):
        self.dao = EventsDAO()

    # Create a new event
    def add_event(self, payload: Dict) -> Dict:
        event = self.dao.create_event(payload)
        if not event:
            raise EventError("Failed to create event.")
        return event

    # Update an event by ID
    def update_event(self, event_id: int, updates: Dict) -> Dict:
        event = self.dao.update_event(event_id, updates)
        if not event:
            raise EventError(f"Event with ID {event_id} not found.")
        return event

    # Delete an event by ID
    def delete_event(self, event_id: int) -> Dict:
        event = self.dao.delete_event(event_id)
        if not event:
            raise EventError(f"Event with ID {event_id} not found.")
        return event

    # Get event by ID
    def get_event(self, event_id: int) -> Dict:
        event = self.dao.get_event_by_id(event_id)
        if not event:
            raise EventError(f"Event with ID {event_id} not found.")
        return event

    # List all events (optional filters)
    def list_events(self, filters: Dict = None) -> List[Dict]:
        events = self.dao.list_events()
        if filters:
            filtered = []
            for e in events:
                match = True
                for k, v in filters.items():
                    if str(e.get(k)).lower() != str(v).lower():
                        match = False
                        break
                if match:
                    filtered.append(e)
            return filtered
        return events
