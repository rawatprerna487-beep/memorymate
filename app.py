import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="reminder_refresh")

st.set_page_config(
    page_title="MemoryMate",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 MemoryMate")
st.caption("Daily Memory & Routine Assistant")
st.write(
    "A simple digital assistant for organizing daily routines, "
    "reminders, and important information."
)

st.info(
    "Educational prototype using fictional information. "
    "It is not intended for diagnosis or medical decision-making."
)
st.header("Today's Schedule")

st.info("No activities added yet.")

if "activities" not in st.session_state:
    st.session_state.activities = []

st.header("Next Reminder")

if st.session_state.activities:
    now = datetime.now().time()

    upcoming = [
        item for item in st.session_state.activities
        if item[1] >= now
    ]

    if upcoming:
        next_item = min(upcoming, key=lambda x: x[1])
        item, time = next_item

        st.info(
            f"Next reminder: {time.strftime('%I:%M %p')} — {item}"
        )
    else:
        st.success("No more reminders for today.")
else:
    st.success("No reminders scheduled.")

if "activities" not in st.session_state:
    st.session_state.activities = []

st.header("Add an Activity")

activity = st.text_input("What would you like to remember?")
activity_time = st.time_input("What time?")

if st.button("Add Activity"):
    if activity:
        st.session_state.activities.append(
            (activity, activity_time)
        )
        st.success("Activity added successfully.")
        st.rerun()
    else:
        st.warning("Please enter an activity first.")

st.header("Today's Activities")

if st.session_state.activities:
    for i, (item, time) in enumerate(st.session_state.activities):
        done = st.checkbox(
            f"{time.strftime('%I:%M %p')} — {item}",
            key=f"activity_{i}"
        )

        if done:
            st.success("✓ Done")
        else:
            st.info("✗ Not done")
else:
    st.info("No activities added yet.")
if st.button("🧹 Clear Completed Activities"):
    remaining = []

    for i, activity in enumerate(st.session_state.activities):
        if not st.session_state.get(f"activity_{i}", False):
            remaining.append(activity)

    st.session_state.activities = remaining
    st.rerun()

if st.session_state.activities:
    current_time = datetime.now().time()

    for i, (item, scheduled_time) in enumerate(st.session_state.activities):

        if current_time >= scheduled_time:
    if not st.session_state.get(f"reminded_{i}", False):
        st.warning(f"🔔 Reminder: {item}")
        st.session_state[f"reminded_{i}"] = True
        else:
            st.info(
                f"🔔 Reminder scheduled: {item} at "
                f"{scheduled_time.strftime('%I:%M %p')}"
            )
else:
    st.info("🔔 No reminders scheduled.") 

    
components.html("""
<button onclick="playReminder()" style="
    padding:10px 18px;
    font-size:16px;
    border-radius:8px;
    border:1px solid #ccc;
    background:#f5f5f5;
    cursor:pointer;">
    🔔 Play Gentle Reminder
</button>

<script>
function playReminder() {
    const audio = new (window.AudioContext || window.webkitAudioContext)();

    const oscillator = audio.createOscillator();
    const gain = audio.createGain();

    oscillator.type = "sine";
    oscillator.frequency.value = 660;

    gain.gain.setValueAtTime(0.12, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audio.currentTime + 0.8
    );

    oscillator.connect(gain);
    gain.connect(audio.destination);

    oscillator.start();
    oscillator.stop(audio.currentTime + 0.8);
}
</script>
""", height=70)
st.header("📝 Memory Notes")

if "memory_notes" not in st.session_state:
    st.session_state.memory_notes = []

note = st.text_input(
    "What would you like to remember?",
    key="memory_note_input"
)
if st.button("Add Note"):
    if note:
        st.session_state.memory_notes.append(note)
        st.success("Note added successfully.")
        st.rerun()
    else:
        st.warning("Please enter a note first.")

if st.session_state.memory_notes:
    st.subheader("Saved Notes")

    for saved_note in st.session_state.memory_notes:
        st.info(f"📝 {saved_note}")
else:
    st.info("No memory notes added yet.")
st.header("👥 Important People")

if "important_people" not in st.session_state:
    st.session_state.important_people = []

person_name = st.text_input(
    "Name",
    key="person_name"
)

relationship = st.text_input(
    "Relationship",
    key="person_relationship"
)

contact = st.text_input(
    "Contact",
    key="person_contact"
)

if st.button("Add Person"):
    if person_name and relationship and contact:
        st.session_state.important_people.append(
            (person_name, relationship, contact)
        )
        st.success("Person added successfully.")
        st.rerun()
    else:
        st.warning("Please fill in all three fields.")

if st.session_state.important_people:
    st.subheader("Saved People")

    for name, relation, phone in st.session_state.important_people:
        st.info(
            f"👤 **{name}**\n\n"
            f"Relationship: {relation}\n\n"
            f"Contact: {phone}"
        )
else:
    st.info("No important people added yet.")
st.header("📅 Important Dates")

if "important_dates" not in st.session_state:
    st.session_state.important_dates = []
date_name = st.text_input(
    "What is the important date?",
    key="date_name"
)

date_value = st.date_input(
    "Select the date",
    key="date_value"
)
if st.button("Add Important Date"):
    if date_name:
        st.session_state.important_dates.append(
            (date_name, date_value)
        )
        st.success("Important date added successfully.")
        st.rerun()
    else:
        st.warning("Please enter a date name first.")
st.subheader("Saved Important Dates")

if st.session_state.important_dates:
    for name, date in st.session_state.important_dates:
        st.info(
            f"📅 **{name}** — {date.strftime('%d %B %Y')}"
        )
else:
    st.info("No important dates added yet.")
from datetime import date

st.subheader("Countdown")

today = date.today()

if st.session_state.important_dates:
    for name, saved_date in st.session_state.important_dates:

        try:
            next_date = saved_date.replace(year=today.year)

            if next_date < today:
                next_date = saved_date.replace(year=today.year + 1)

            days_left = (next_date - today).days

            if days_left == 0:
                st.success(f"🎉 Today is {name}!")
            else:
                st.info(
                    f"📅 **{name}** — {days_left} days remaining"
                )

        except ValueError:
            st.info(f"📅 **{name}** — Date reminder saved.")
from datetime import date

st.subheader("Countdown")

today = date.today()

if st.session_state.important_dates:
    for name, saved_date in st.session_state.important_dates:

        try:
            next_date = saved_date.replace(year=today.year)

            if next_date < today:
                next_date = saved_date.replace(year=today.year + 1)

            days_left = (next_date - today).days

            if days_left == 0:
                st.success(f"🎉 Today is {name}!")
            else:
                st.info(
                    f"📅 **{name}** — {days_left} days remaining"
                )

        except ValueError:
            st.info(f"📅 **{name}** — Date reminder saved.")
if st.button("🧹 Clear Important Dates"):
    st.session_state.important_dates = []
    st.rerun()
