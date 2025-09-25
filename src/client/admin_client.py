# src/cli/admin_cli.py
import argparse
import json
from src.services.event_services import EventService

class AdminCLI:
    def __init__(self):
        self.event_service = EventService()

    # --- EVENT COMMANDS ---
    def cmd_event_add(self, args):
        payload = {
            "event_name": args.name,
            "event_date": args.date,
            "location": args.location,
            "description": args.description
        }
        event = self.event_service.add_event(payload)
        print("✅ Event created:")
        print(json.dumps(event, indent=2, default=str))

    def cmd_event_list(self, args):
        events = self.event_service.list_events()
        print("📅 All Events:")
        print(json.dumps(events, indent=2, default=str))


def build_admin_parser():
    parser = argparse.ArgumentParser(prog="admin-cli")
    sub = parser.add_subparsers(dest="entity")

    cli = AdminCLI()

    # --- EVENTS ---
    event_parser = sub.add_parser("event")
    event_sub = event_parser.add_subparsers(dest="action")

    # Add Event
    add_e = event_sub.add_parser("add")
    add_e.add_argument("--name", required=True)
    add_e.add_argument("--date", required=True)
    add_e.add_argument("--location")
    add_e.add_argument("--description")
    add_e.set_defaults(func=cli.cmd_event_add)

    # List Events
    list_e = event_sub.add_parser("list")
    list_e.set_defaults(func=cli.cmd_event_list)

    return parser


def main():
    parser = build_admin_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
