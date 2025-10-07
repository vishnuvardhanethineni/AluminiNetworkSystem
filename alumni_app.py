import streamlit as st
from src.services.alumni_services import AlumniService, AlumniError
from src.services.event_services import EventService, EventError
from src.services.mentorship_services import MentorshipServices, MentorshipError

st.set_page_config(page_title="🎓 Alumni Portal", layout="wide")
st.title("🎓 Alumni Portal — Alumni Network System")

alumni_service = AlumniService()
event_service = EventService()
mentorship_service = MentorshipServices()

menu = st.sidebar.selectbox(
    "Select a section",
    ["Home", "Profile", "Mentorship", "Events"]
)

# ------------------------------
# HOME
# ------------------------------
if menu == "Home":
    st.header("Welcome, Alumni!")
    st.write("""
        - Register and manage your alumni profile  
        - Become a mentor and guide students  
        - Host events for the community  
    """)

# ------------------------------
# PROFILE
# ------------------------------
elif menu == "Profile":
    st.header("Alumni Profile")

    tab1, tab2 = st.tabs(["➕ Register", "📋 View Alumni"])

    with tab1:
        with st.form("add_alumni"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            industry = st.text_input("Industry")
            graduation_year = st.number_input("Graduation Year", min_value=1900, max_value=2100, step=1)
            location = st.text_input("Location")
            submitted = st.form_submit_button("Add")
            if submitted:
                payload = {
                    "name": name,
                    "email": email,
                    "industry": industry,
                    "graduation_year": graduation_year,
                    "location": location
                }
                try:
                    alumni = alumni_service.add_alumni(payload)
                    st.success(f"✅ Alumni registered: {alumni['name']}")
                except AlumniError as e:
                    st.error(str(e))

    with tab2:
        try:
            alumni_list = alumni_service.list_alumni()
            if alumni_list:
                st.selectbox("Select Alumni to View", options=[f"{a['alumni_id']} - {a['name']}" for a in alumni_list])
                st.table(alumni_list)
            else:
                st.info("No alumni found.")
        except AlumniError as e:
            st.error(str(e))

# ------------------------------
# MENTORSHIP
# ------------------------------
elif menu == "Mentorship":
    st.header("🧑‍🏫 Mentorship")

    tab1, tab2 = st.tabs(["Become Mentor", "View My Mentees"])

    with tab1:
        st.subheader("Register as Mentor")
        try:
            alumni_list = alumni_service.list_alumni()
            alumni_options = {f"{a['alumni_id']} - {a['name']}": a['alumni_id'] for a in alumni_list}
            selected = st.selectbox("Select Your Alumni", options=list(alumni_options.keys()))
            alumni_id = alumni_options[selected]
            skills = st.text_input("Skills (comma separated)")
            if st.button("Become Mentor"):
                mentor = mentorship_service.create_mentor(alumni_id, skills)
                st.success(f"✅ Mentor created successfully! Mentor ID: {mentor['mentor_id']}")
        except AlumniError as e:
            st.error(str(e))
        except MentorshipError as e:
            st.error(str(e))

    # Mentorship tab
elif menu == "Mentorship":
    st.header("🧑‍🏫 Mentorship")

    tab1, tab2 = st.tabs(["Become Mentor", "View My Mentees"])

    # --- Become Mentor ---
    with tab1:
        st.subheader("Register as Mentor")
        try:
            alumni_list = alumni_service.list_alumni()
            if alumni_list:
                # Dropdown for selecting your alumni ID
                alumni_options = {f"{a['alumni_id']} - {a['name']}": a['alumni_id'] for a in alumni_list}
                selected_alumni = st.selectbox("Select Your Alumni ID", list(alumni_options.keys()))
                skills = st.text_input("Skills (comma separated)")
                if st.button("Become Mentor"):
                    if selected_alumni:
                        alumni_id = alumni_options[selected_alumni]
                        try:
                            mentor = mentorship_service.create_mentor(alumni_id, skills)
                            st.success(f"✅ Mentor created successfully! Mentor ID: {mentor['mentor_id']}")
                        except MentorshipError as e:
                            st.error(str(e))
            else:
                st.info("No alumni available. Add alumni first!")
        except Exception as e:
            st.error(str(e))

    # --- View My Mentees ---
    with tab2:
        st.subheader("My Mentees")
        try:
            mentors_list = mentorship_service.list_mentors()
            if mentors_list:
                mentor_options = {f"{m['mentor_id']} - Alumni {m['alumni_id']}": m['mentor_id'] for m in mentors_list}
                selected_mentor = st.selectbox("Select Your Mentor", list(mentor_options.keys()))
                if selected_mentor:
                    mentor_id = mentor_options[selected_mentor]
                    if st.button("View Mentees"):
                        mentees = mentorship_service.list_students_by_mentor(mentor_id)
                        if mentees:
                            st.table(mentees)
                        else:
                            st.info("No mentees found for this mentor.")
            else:
                st.info("No mentors available. Become a mentor first!")
        except MentorshipError as e:
            st.error(str(e))




# ------------------------------
# EVENTS
# ------------------------------
elif menu == "Events":
    st.header("🎉 Event Management")

    tab1, tab2 = st.tabs(["List Events", "Join Event"])

    with tab1:
        st.subheader("All Events")
        try:
            events = alumni_service.search_events()
            if events:
                st.table(events)
            else:
                st.info("No events available.")
        except AlumniError as e:
            st.error(str(e))

    with tab2:
        st.subheader("Join Event")
        try:
            events = alumni_service.search_events()
            event_options = {f"{e['event_id']} - {e['event_name']}": e['event_id'] for e in events}
            selected_event = st.selectbox("Select Event", options=list(event_options.keys()))
            event_id = event_options[selected_event]

            alumni_list = alumni_service.list_alumni()
            alumni_options = {f"{a['alumni_id']} - {a['name']}": a['alumni_id'] for a in alumni_list}
            selected_alumni = st.selectbox("Select Yourself", options=list(alumni_options.keys()))
            alumni_id = alumni_options[selected_alumni]

            if st.button("Join Event"):
                registration = alumni_service.join_event(alumni_id, event_id)
                st.success(f"✅ Successfully joined event ID {event_id}")
        except AlumniError as e:
            st.error(str(e))
