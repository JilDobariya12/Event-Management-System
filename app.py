import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# 🔗 API Configuration
# -----------------------------
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Event Management Dashboard", page_icon="🎭", layout="wide")

# -----------------------------
# 🎭 Header
# -----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b;'>
        🎭 Event Management Dashboard
    </h1>
    <p style='text-align: center; color: gray;'>
        Manage Attendees, Venues, and Events seamlessly 💼
    </p>
""", unsafe_allow_html=True)

# -----------------------------
# 🗂️ Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["👥 Attendees", "🏛️ Venues", "🎫 Events"])

# =========================================
# TAB 1 — ATTENDEES
# =========================================
with tab1:
    st.subheader("👥 Manage Attendees")

    col1, col2 = st.columns([2, 3])
    with col1:
        with st.form("add_attendee"):
            st.markdown("### ➕ Add New Attendee")
            name = st.text_input("Name")
            atype = st.selectbox("Type", ["Student", "Guest", "VIP"])
            pstatus = st.selectbox("Payment Status", ["Paid", "Pending"])
            submit_attendee = st.form_submit_button("Add Attendee")

            if submit_attendee:
                if name.strip():
                    res = requests.post(
                        f"{API_URL}/attendees",
                        json={"name": name, "type": atype, "payment_status": pstatus},
                    )
                    if res.status_code == 200:
                        st.success(f" Attendee '{name}' added successfully!")
                    else:
                        st.error(" Error adding attendee. Check backend logs.")
                else:
                    st.warning("Please enter a valid name!")

    with col2:
        if st.button("📋 Show All Attendees"):
            try:
                attendees = requests.get(f"{API_URL}/attendees").json()
                if attendees:
                    st.dataframe(attendees, use_container_width=True)
                else:
                    st.info("No attendees found.")
            except Exception as e:
                st.error(f"Failed to fetch attendees: {e}")

# =========================================
# TAB 2 — VENUES
# =========================================
with tab2:
    st.subheader("🏛️ Manage Venues")

    col1, col2 = st.columns([2, 3])
    with col1:
        with st.form("add_venue"):
            st.markdown("### 🏗️ Add New Venue")
            vname = st.text_input("Venue Name")
            layout = st.text_area("Layout Info")
            capacity = st.number_input("Capacity", min_value=10)
            security_id = st.number_input("Security ID (optional)", min_value=0, value=0)
            design_id = st.number_input("Design ID (optional)", min_value=0, value=0)
            submit_venue = st.form_submit_button("Add Venue")

            if submit_venue:
                if vname.strip():
                    res = requests.post(
                        f"{API_URL}/venues",
                        json={"name": vname, "layout": layout, "capacity": capacity,
                              "security_id": security_id or None,
                              "design_id": design_id or None
                              },
                    )
                    if res.status_code == 200:
                        st.success(f"🏛️ Venue '{vname}' added successfully!")
                    else:
                        st.error("Error adding venue. Check backend logs.")
                else:
                    st.warning("⚠Please enter a valid venue name!")

    with col2:
        if st.button("📋 Show All Venues"):
            try:
                venues = requests.get(f"{API_URL}/venues").json()
                if venues:
                    st.dataframe(venues, use_container_width=True)
                else:
                    st.info("No venues found.")
            except Exception as e:
                st.error(f"Failed to fetch venues: {e}")

# =========================================
# TAB 3 — EVENTS (View Only)
# =========================================
with tab3:
    st.subheader("🎫 All Upcoming Events")

    try:
        events = requests.get(f"{API_URL}/events").json()

        if events:
            for event in events:
                with st.expander(f"{event['event_name']} | {event['date_time']} | Venue ID: {event['venue_id']}"):
                    st.write(f"📅 Date & Time: {event['date_time']}")
                    st.write(f"🏛️ Venue ID: {event['venue_id']}")
                    st.write(f"👥 Volunteer ID: {event.get('volunteer_id')}")
                    st.write(f"💰 Finance ID: {event.get('finance_id')}")

        else:
            st.info("No events found.")
    except Exception as e:
        st.error(f"Failed to fetch events: {e}")

# --------------------------------------------
# 🖋️ Footer
# --------------------------------------------
st.markdown("""
    <hr style='margin-top: 50px;'>
    <div style='text-align: right; color: gray; font-size: 14px;'>
        Made with ❤️ by <b>Jil Dobariya</b>
    </div>
""", unsafe_allow_html=True)

#Streamlit app (frontend): Sends HTTP requests to FastAPI using the requests library.