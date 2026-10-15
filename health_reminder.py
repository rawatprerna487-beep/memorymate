import streamlit as st
from datetime import datetime

def show_health_reminder():
    st.title("🌿 Daily Health Dashboard")
    st.caption("A gentle space for daily routines and medicine reminders.")

    st.info(
        "Educational prototype only. Enter medicine schedules "
        "according to instructions from your healthcare professional."
    )

    if "medicines" not in st.session_state:
        st.session_state.medicines = []

    st.subheader("💊 Medicine Reminder")

    with st.form("add_medicine_form"):
        name = st.text_input("Medicine name")
        schedule = st.text_input(
            "Prescribed schedule",
            placeholder="As written on your prescription"
        )
        reminder_time = st.time_input(
            "Reminder time",
            value=datetime.strptime("08:00", "%H:%M").time()
        )
        submitted = st.form_submit_button("Add Medicine Reminder")

        if submitted:
            if name.strip() and schedule.strip():
                st.session_state.medicines.append({
                    "name": name.strip(),
                    "schedule": schedule.strip(),
                    "time": reminder_time.strftime("%I:%M %p"),
                    "status": "Not yet"
                })
                st.success("Reminder added for this session.")
            else:
                st.warning("Please enter the medicine name and schedule.")

    st.subheader("Today's Medicine Reminders")

    if not st.session_state.medicines:
        st.info("No medicine reminders added yet.")
    else:
        for i, medicine in enumerate(st.session_state.medicines):
            with st.container(border=True):
                st.write(f"**{medicine['name']}**")
                st.caption(f"Schedule: {medicine['schedule']}")
                st.write(f"🔔 Reminder time: {medicine['time']}")

                status = st.selectbox(
                    "Record status",
                    ["Not yet", "Taken", "Not sure"],
                    index=["Not yet", "Taken", "Not sure"].index(
                        medicine["status"]
                    ),
                    key=f"medicine_status_{i}"
                )
                st.session_state.medicines[i]["status"] = status

    st.divider()
    st.caption(
        "Statuses are entered by the user and do not verify "
        "whether a medicine was actually taken."
    )

def show_daily_companion():
    st.title("🌿 My Daily Companion")
    st.caption("Gentle support for everyday life and routines.")

    st.info(
        "This is a supportive educational prototype. "
        "A caregiver can help set up familiar routines."
    )

    # 1. Where Am I?
    st.subheader("📅 Where Am I?")
    now = datetime.now()

    st.write(f"**Today:** {now.strftime('%A, %d %B %Y')}")
    st.write(f"**Current time:** {now.strftime('%I:%M %p')}")

    familiar_place = st.text_input(
        "A familiar place or helpful message",
        placeholder="Example: You are at home with your family."
    )

    if familiar_place.strip():
        st.info(f"💚 Remember: {familiar_place}")

    st.divider()

    # 2. My Daily Routine
    st.subheader("🗓️ My Daily Routine")
    st.write("Add familiar activities in the order they should happen.")

    if "companion_routine" not in st.session_state:
        st.session_state.companion_routine = []

    with st.form("companion_routine_form"):
        activity = st.text_input(
            "Activity",
            placeholder="Example: Have breakfast"
        )
        activity_time = st.text_input(
            "Time",
            placeholder="Example: 8:00 AM"
        )
        routine_added = st.form_submit_button("Add Activity")

        if routine_added:
            if activity.strip() and activity_time.strip():
                st.session_state.companion_routine.append({
                    "activity": activity.strip(),
                    "time": activity_time.strip()
                })
                st.success("Activity added.")
            else:
                st.warning("Please enter both the activity and time.")

    routine = st.session_state.companion_routine

    if routine:
        for number, item in enumerate(routine, start=1):
            st.write(
                f"**{number}. {item['time']}** — {item['activity']}"
            )
    else:
        st.info("Your daily routine will appear here after activities are added.")

    st.divider()

    # 3. What Should I Do Next?
    st.subheader("➡️ What Should I Do Next?")

    if routine:
        if "companion_step" not in st.session_state:
            st.session_state.companion_step = 0

        st.session_state.companion_step = min(
            st.session_state.companion_step, len(routine) - 1
        )

        current_step = st.session_state.companion_step
        current_activity = routine[current_step]

        st.markdown("### One step at a time")
        st.info(
            f"**{current_activity['activity']}**\n\n"
            f"Usual time: {current_activity['time']}"
        )

        left, right = st.columns(2)

        with left:
            if st.button("🔊 Repeat", key="repeat_companion_step"):
                st.info(
                    f"Your next activity is: {current_activity['activity']}"
                )

        with right:
            if st.button("Next ➡️", key="next_companion_step"):
                st.session_state.companion_step = (
                    current_step + 1
                ) % len(routine)
                st.rerun()
    else:
        st.info("Add activities to see one step at a time.")

    st.divider()

    # 4. How Am I Feeling?
    st.subheader("💚 How Am I Feeling?")

    feeling = st.radio(
        "Choose the option that best describes how you feel:",
        [
            "😊 I feel good",
            "😔 I feel sad",
            "😟 I feel worried",
            "😣 I feel uncomfortable",
            "🆘 I need help"
        ],
        key="companion_feeling"
    )

    if st.button("Share How I Feel"):
        if "I need help" in feeling:
            st.warning(
                "Please tell a trusted caregiver or nearby person "
                "that you need help."
            )
        elif "uncomfortable" in feeling:
            st.info(
                "Please tell your caregiver what feels uncomfortable."
            )
        else:
            st.success(f"Your selected feeling: {feeling}")

    st.caption(
        "This page does not detect your physical location or provide "
        "medical diagnoses. Information and routines are entered by "
        "the user or caregiver."
    )
