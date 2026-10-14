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
