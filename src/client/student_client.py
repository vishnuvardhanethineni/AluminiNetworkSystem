# src/cli/student_cli.py
import json
import argparse
from src.services.student_services import StudentService, StudentError
class StudentCLI:
    def __init__(self):
        self.service = StudentService()

    def cmd_add_student(self, args):
        try:
            student = self.service.create_student(args.name, args.email, args.course, args.year)
            print("Student added:")
            print(json.dumps(student, indent=2, default=str))
        except StudentError as e:
            print("Error:", e)

    def cmd_update_student(self, args):
        updates = {}
        if args.name: updates["name"] = args.name
        if args.email: updates["email"] = args.email
        if args.course: updates["course"] = args.course
        if args.year: updates["year"] = args.year
        try:
            student = self.service.update_student(args.student_id, updates)
            print("Student updated:")
            print(json.dumps(student, indent=2, default=str))
        except StudentError as e:
            print("Error:", e)

    def cmd_delete_student(self, args):
        try:
            student = self.service.delete_student(args.student_id)
            print("Student deleted:")
            print(json.dumps(student, indent=2, default=str))
        except StudentError as e:
            print("Error:", e)

    def cmd_list_students(self, args):
        filters = {}
        if args.name: filters["name"] = args.name
        if args.email: filters["email"] = args.email
        if args.course: filters["course"] = args.course
        if args.year: filters["year"] = args.year

        students = self.service.list_students(filters if filters else None)
        print("Student list:")
        print(json.dumps(students, indent=2, default=str))
    # --- Event commands ---
    def cmd_search_events(self, args):
        filters = {}
        if args.name: filters["event_name"] = args.name
        if args.event_date: filters["event_date"] = args.event_date
        try:
            events = self.service.search_events(filters if filters else None)
            print("📅 Events:")
            print(json.dumps(events, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)

    def cmd_join_event(self, args):
        try:
            reg = self.service.join_event(args.student_id, args.event_id)
            print(f"🎉 Student {args.student_id} joined event {args.event_id}:")
            print(json.dumps(reg, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)

    def cmd_list_my_events(self, args):
        try:
            events = self.service.list_my_events(args.student_id)
            print(f"📌 Events for student {args.student_id}:")
            print(json.dumps(events, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)

    
    def cmd_list_mentors(self, args):
        try:
            mentors = self.service.list_mentors()  # use StudentService
            print("📋 Mentors list:")
            print(json.dumps(mentors, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)

    def cmd_join_mentorship(self, args):
        try:
            assignment = self.service.join_mentorship(
                args.student_id, args.mentor_id, args.start_date, args.end_date
            )
            print(f"✅ Student {args.student_id} assigned to mentor {args.mentor_id}:")
            print(json.dumps(assignment, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)

    def cmd_list_my_mentors(self, args):
        try:
            assignments = self.service.list_my_mentors(args.student_id)
            print(f"📌 Mentors for student {args.student_id}:")
            print(json.dumps(assignments, indent=2, default=str))
        except StudentError as e:
            print("❌ Error:", e)
    

def build_parser():
    cli = StudentCLI()
    parser = argparse.ArgumentParser(prog="student-cli")
    sub = parser.add_subparsers(dest="command")

    # Add student
    addp = sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--email", required=True)
    addp.add_argument("--course", default=None)
    addp.add_argument("--year", type=int, default=None)
    addp.set_defaults(func=cli.cmd_add_student)

    # Update student
    updatep = sub.add_parser("update")
    updatep.add_argument("--student_id", type=int, required=True)
    updatep.add_argument("--name", default=None)
    updatep.add_argument("--email", default=None)
    updatep.add_argument("--course", default=None)
    updatep.add_argument("--year", type=int, default=None)
    updatep.set_defaults(func=cli.cmd_update_student)

    # Delete student
    deletep = sub.add_parser("delete")
    deletep.add_argument("--student_id", type=int, required=True)
    deletep.set_defaults(func=cli.cmd_delete_student)

    # List students
    listp = sub.add_parser("list")
    listp.add_argument("--name", default=None)
    listp.add_argument("--email", default=None)
    listp.add_argument("--course", default=None)
    listp.add_argument("--year", type=int, default=None)
    listp.set_defaults(func=cli.cmd_list_students)
    # Event commands
    ev_search = sub.add_parser("events-search")
    ev_search.add_argument("--name")
    ev_search.add_argument("--event_date")
    ev_search.set_defaults(func=cli.cmd_search_events)

    ev_join = sub.add_parser("join-event")
    ev_join.add_argument("--student_id", type=int, required=True)
    ev_join.add_argument("--event_id", type=int, required=True)
    ev_join.set_defaults(func=cli.cmd_join_event)

    ev_list = sub.add_parser("my-events")
    ev_list.add_argument("--student_id", type=int, required=True)
    ev_list.set_defaults(func=cli.cmd_list_my_events)

    mentors_list = sub.add_parser("mentors-list")
    mentors_list.set_defaults(func=cli.cmd_list_mentors)

    join_mentorship = sub.add_parser("join-mentorship")
    join_mentorship.add_argument("--student_id", type=int, required=True)
    join_mentorship.add_argument("--mentor_id", type=int, required=True)
    join_mentorship.add_argument("--start_date", default=None)
    join_mentorship.add_argument("--end_date", default=None)
    join_mentorship.set_defaults(func=cli.cmd_join_mentorship)

    list_my_mentors = sub.add_parser("my-mentors")
    list_my_mentors.add_argument("--student_id", type=int, required=True)
    list_my_mentors.set_defaults(func=cli.cmd_list_my_mentors)


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
