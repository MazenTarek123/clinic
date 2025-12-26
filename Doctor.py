import streamlit as st

# ---------------------------------------------------------
# Hide Streamlit Default UI
# ---------------------------------------------------------
hide_streamlit_elements = """
<style>
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
</style>
"""
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cure & Go | Doctor",
    page_icon="👨‍⚕️",
    layout="wide"
)

# ---------------------------------------------------------
# Global Styling (نفس admin)
# ---------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    font-family: 'Segoe UI', sans-serif;
}
.main-title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    color: #1f2937;
    animation: fadeDown 1s ease;
}
.sub-title {
    text-align: center;
    color: #374151;
    margin-bottom: 30px;
}
.stButton>button {
    border-radius: 14px;
    padding: 10px;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
}
@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Doctor Function
# ---------------------------------------------------------
def doctor_function():

    # ------------------ Login ------------------
    if st.session_state.get("logged_in_doctor") is None:

        st.markdown("<div class='main-title'>👨‍⚕️ Doctor Login</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>Cure & Go Medical Center</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            doc_id = st.text_input("Doctor ID (3 digits)")
            if st.button("Login", use_container_width=True):

                if len(doc_id) == 3 and doc_id.isdigit():
                    found = None
                    for d in st.session_state.get("all_doctors", []):
                        if d.doctor_id == doc_id:
                            found = d
                            break

                    if found:
                        st.session_state.logged_in_doctor = found
                        st.success(f"Welcome Dr. {found.name} 👋")
                        st.rerun()
                    else:
                        st.error("Doctor ID not found ❌")
                else:
                    st.error("ID must be exactly 3 digits")

        return

    # ------------------ Dashboard ------------------
    doctor = st.session_state.logged_in_doctor

    st.markdown(f"<div class='main-title'>👨‍⚕️ Dr. {doctor.name}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='sub-title'>{doctor.specialization}</div>",
        unsafe_allow_html=True
    )

    st.sidebar.title("Doctor Panel")
    menu = st.sidebar.radio(
        "Navigation",
        ["📅 My Appointments", "⚙️ Manage Availability", "🚪 Logout"]
    )

    # ------------------ Appointments ------------------
    if menu == "📅 My Appointments":
        st.subheader("📅 My Scheduled Appointments")

        my_apps = [
            a for a in st.session_state.get("appointments", [])
            if a["doctor_id"] == doctor.doctor_id
        ]

        if my_apps:
            table_data = []
            for a in my_apps:
                table_data.append({
                    "Patient": a["patient_name"],
                    "Phone": a["patient_phone"],
                    "Day": a["day"],
                    "Time": f"{a['hour']}:00"
                })
            st.table(table_data)
        else:
            st.info("No appointments yet.")

    # ------------------ Availability ------------------
    elif menu == "⚙️ Manage Availability":
        st.subheader("⚙️ Edit Availability")

        day = st.selectbox("Select Day", list(doctor.schedule.keys()))
        schedule = doctor.schedule[day]

        st.info("Booked hours cannot be modified")

        col1, col2, col3 = st.columns(3)

        for hour in range(24):
            status = schedule[hour]
            label = f"{hour:02d}:00"

            col = col1 if hour < 8 else col2 if hour < 16 else col3

            with col:
                if status == "booked":
                    st.warning(f"{label} 🔒 Booked")
                else:
                    is_open = status == "available"
                    btn = f"{label} {'✅ Open' if is_open else '⛔ Closed'}"

                    if st.button(btn, key=f"{day}_{hour}"):
                        schedule[hour] = "not available" if is_open else "available"
                        st.toast("Schedule Updated ✅")
                        st.rerun()

    # ------------------ Logout ------------------
    elif menu == "🚪 Logout":
        st.session_state.logged_in_doctor = None
        st.rerun()
