# src/cli/alumni_cli.py
import json
from src.services.alumni_services import AlumniService, AlumniError
from src.services.mentorship_services import MentorshipServices, MentorshipError
class AlumniCLI:
    def __init__(self):
        self.alumni_service = AlumniService()
        self.mentor_service = MentorshipServices()

    # Alumni commands
    def cmd_add_alumni(self, args):
        payload = {
            "name": args.name,
            "email": args.email,
            "industry": args.industry,
            "graduation_year": args.graduation_year,
            "location": args.location
        }
        try:
            a = self.alumni_service.add_alumni(payload)
            print("✅ Alumni added:")
            print(json.dumps(a, indent=2, default=str))
        except AlumniError as e:

            print("❌ Error:", e)

    def cmd_update_alumni(self, args):
        updates = {}
        if args.name: updates["name"] = args.name
        if args.email: updates["email"] = args.email
        if args.industry: updates["industry"] = args.industry
        if args.graduation_year: updates["graduation_year"] = args.graduation_year
        if args.location: updates["location"] = args.location
        try:
            a = self.alumni_service.update_alumni(args.alumni_id, updates)
            print("✅ Alumni updated:")
            print(json.dumps(a, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    def cmd_delete_alumni(self, args):
        try:
            a = self.alumni_service.remove_alumni(args.alumni_id)
            print("🗑️ Alumni deleted:")
            print(json.dumps(a, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    def cmd_list_alumni(self, args):
        try:
            a_list = self.alumni_service.list_alumni()
            print("📋 Alumni list:")
            print(json.dumps(a_list, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    def cmd_search_alumni(self, args):
        try:
            results = self.alumni_service.search_alumni(args.field, args.value)
            print("🔍 Search results:")
            print(json.dumps(results, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    # Event commands for alumni
    def cmd_search_events(self, args):
        filters = {}
        if args.name: filters["name"] = args.name
        if args.event_date: filters["event_date"] = args.event_date
        try:
            events = self.alumni_service.search_events(filters if filters else None)
            print("📅 Events:")
            print(json.dumps(events, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    def cmd_join_event(self, args):
        try:
            reg = self.alumni_service.join_event(args.alumni_id, args.event_id)
            print(f"🎉 Alumni {args.alumni_id} joined event {args.event_id}:")
            print(json.dumps(reg, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)

    def cmd_list_my_events(self, args):
        try:
            events = self.alumni_service.list_my_events(args.alumni_id)
            print(f"📌 Events for alumni {args.alumni_id}:")
            print(json.dumps(events, indent=2, default=str))
        except AlumniError as e:
            print("❌ Error:", e)
    def cmd_become_mentor(self, args):
        alumni_id = args.alumni_id
        skills = args.skills

        try:
            # Check if alumni is already a mentor
            existing = self.mentor_service.get_mentor_by_alumni(alumni_id)
            if existing:
                print(f"❌ Alumni ID {alumni_id} is already registered as a mentor.")
                return

            # Register as mentor
            mentor = self.mentor_service.create_mentor(alumni_id, skills)
            print("✅ Alumni registered as mentor successfully:")
            print(json.dumps(mentor, indent=2, default=str))

        except MentorshipError as e:
            print("❌ Error:", e)
    
# Parser
def build_parser():
    import argparse
    cli = AlumniCLI()
    parser = argparse.ArgumentParser(prog="alumni-cli")
    sub = parser.add_subparsers(dest="command")

    # --- Alumni commands ---
    addp = sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--email", required=True)
    addp.add_argument("--industry", required=True)
    addp.add_argument("--graduation_year", type=int, required=True)
    addp.add_argument("--location", required=True)
    addp.set_defaults(func=cli.cmd_add_alumni)

    updatep = sub.add_parser("update")
    updatep.add_argument("--alumni_id", type=int, required=True)
    updatep.add_argument("--name")
    updatep.add_argument("--email")
    updatep.add_argument("--industry")
    updatep.add_argument("--graduation_year", type=int)
    updatep.add_argument("--location")
    updatep.set_defaults(func=cli.cmd_update_alumni)

    deletep = sub.add_parser("delete")
    deletep.add_argument("--alumni_id", type=int, required=True)
    deletep.set_defaults(func=cli.cmd_delete_alumni)

    listp = sub.add_parser("list")
    listp.set_defaults(func=cli.cmd_list_alumni)

    searchp = sub.add_parser("search")
    searchp.add_argument("--field", required=True, help="Field to search by (name, email, industry, location)")
    searchp.add_argument("--value", required=True, help="Value to search for")
    searchp.set_defaults(func=cli.cmd_search_alumni)

    # --- Event commands ---
    ev_search = sub.add_parser("events-search")
    ev_search.add_argument("--name")
    ev_search.add_argument("--event_date")
    ev_search.set_defaults(func=cli.cmd_search_events)

    ev_join = sub.add_parser("join-event")
    ev_join.add_argument("--alumni_id", type=int, required=True)
    ev_join.add_argument("--event_id", type=int, required=True)
    ev_join.set_defaults(func=cli.cmd_join_event)

    ev_list = sub.add_parser("my-events")
    ev_list.add_argument("--alumni_id", type=int, required=True)
    ev_list.set_defaults(func=cli.cmd_list_my_events)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()