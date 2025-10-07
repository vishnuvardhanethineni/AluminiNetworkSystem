import streamlit as st
from src.services.student_services import StudentService, StudentError
from src.services.event_services import EventService, EventError

st.set_page_config(page_title="Student Portal", page_icon="🎓")
st.title("🎓 Student Dashboard")

student_service = StudentService()
event_service = EventService()

tabs = st.tabs([
    "Register Student",
    "Browse & Join Events",
    "Join Mentorship",
    "My Mentors",
    "My Events"
])

# --- Student Registration ---
with tabs[0]:
    st.subheader("Register as Student")
    with st.form("student_reg"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        course = st.text_input("Course")
        year = st.number_input("Year", min_value=1, max_value=5, step=1)
        if st.form_submit_button("Register"):
            try:
                data = student_service.create_student(name, email, course, year)
                st.success(f"Student added successfully: {data['name']}")
            except StudentError as e:
                st.error(f"Error: {e}")

# --- Browse & Join Events ---
with tabs[1]:
    st.subheader("Browse and Join Events")
    try:
        events = event_service.list_events()
        if events:
            for e in events:
                with st.expander(f"{e['event_name']} — {e['event_date']}"):
                    st.write(e["description"])
                    st.write(f"📍 {e['location']}")
                    student_id = st.number_input("Your Student ID", min_value=1, step=1, key=f"join_{e['event_id']}")
                    if st.button(f"Join Event {e['event_id']}", key=f"btn_{e['event_id']}"):
                        try:
                            result = student_service.join_event(student_id, e['event_id'])
                            st.success("Joined successfully!")
                        except StudentError as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No events available right now.")
    except EventError as e:
        st.error(f"Error fetching events: {e}")

# --- Join Mentorship ---
with tabs[2]:
    st.subheader("Join Mentorship Program")
    student_id = st.number_input("Your Student ID", min_value=1, step=1, key="join_mentorship_sid")
    mentor_id = st.number_input("Mentor ID", min_value=1, step=1, key="join_mentorship_mid")
    if st.button("Join Mentorship"):
        try:
            data = student_service.join_mentorship(student_id, mentor_id)
            st.success("Mentorship joined successfully!")
        except StudentError as e:
            st.error(f"Error: {e}")

# --- My Mentors ---
with tabs[3]:
    st.subheader("View My Mentors")
    student_id = st.number_input("Enter Student ID", min_value=1, step=1, key="mentor_list")
    if st.button("Show Mentors"):
        try:
            mentors = student_service.get_student_mentors(student_id)
            if mentors:
                st.table(mentors)
            else:
                st.info("No mentors assigned yet.")
        except StudentError as e:
            st.error(f"Error: {e}")

# --- My Events ---
with tabs[4]:
    st.subheader("My Registered Events")
    student_id = st.number_input("Enter Student ID", min_value=1, step=1, key="event_list")
    if st.button("Show My Events"):
        try:
            events = student_service.list_my_events(student_id)
            if events:
                st.table(events)
            else:
                st.info("No events joined yet.")
        except StudentError as e:
            st.error(f"Error: {e}")
