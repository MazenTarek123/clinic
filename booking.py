import streamlit as st

# ---------------- Hide Streamlit UI ----------------
hide_streamlit_elements = """
<style>
header {visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

.main > div {
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
"""
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Cure & Go | Patient Booking",
    page_icon="🧑‍🦱",
    layout="wide"
)

# ---------------- Design (SAME AS ADMIN) ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f2937;
    animation: fadeDown 1s ease;
}

.sub-title {
    text-align: center;
    color: #374151;
    margin-bottom: 35px;
    font-size: 18px;
}

.stButton>button {
    border-radius: 14px;
    padding: 12px;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.06);
}

input, textarea {
    color: #111827 !important;
}

div[data-baseweb="select"] span {
    color: #111827 !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px;
    border: 1px solid #d1d5db;
}

.stRadio label {
    color: #1f2937 !important;
    font-weight: 600;
}

table, th, td {
    color: #111827 !important;
}

@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- Get Disease From URL ----------------
query_params = st.query_params
selected_disease = query_params.get("disease", "General Consultation")
if isinstance(selected_disease, list):
    selected_disease = selected_disease[0]

# ---------------- Header ----------------
st.markdown("<div class='main-title'>🧑‍🦱 Patient Booking</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='sub-title'>📌 Booking for <b>{selected_disease}</b></div>",
    unsafe_allow_html=True
)

# ---------------- Session State ----------------
if "doctors" not in st.session_state:
    st.session_state.doctors = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "patients" not in st.session_state:
    st.session_state.patients = []

if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# ---------------- Doctor Class ----------------
class Doctor:
    def __init__(self, doctor_id, name, specialization, room, price):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.room = room
        self.price = price

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = ["09", "10", "11", "12", "14", "15", "16", "17"]
        self.schedule = {day: {hour: "available" for hour in hours} for day in days}

# ---------------- Doctors Data ----------------
if not st.session_state.doctors:
    st.session_state.doctors = [
        Doctor("001", "Haneen El-Barbary", "Psychotherapy", 1, 250),
        Doctor("002", "Haneen Ayman", "Pediatrics", 2, 200),
        Doctor("003", "Menna Ayman", "Dermatology", 3, 300),
        Doctor("004", "Sohaila Gomaa", "ENT", 4, 220),
        Doctor("005", "Nour Omar", "Nutrition", 5, 180),
        Doctor("006", "Haneen El Azab", "Cardiology", 6, 350),
        Doctor("007", "Mostafa Hatem", "Orthopedics", 7, 300),
        Doctor("008", "Mazen Tarek", "Neurology", 8, 350),
    ]

# ---------------- Login / Register ----------------
st.markdown("### 👤 Patient Access")

option = st.radio("Choose option", ["Login", "Create Account"], horizontal=True)

if option == "Create Account":
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        phone = st.text_input("Phone Number")

    if st.button("Create Account", use_container_width=True):
        if name and phone:
            patient = {
                "name": name,
                "phone": phone,
                "appointments": []
            }
            st.session_state.patients.append(patient)
            st.session_state.current_patient = patient
            st.success(f"Welcome {name} 👋")

if option == "Login":
    phone = st.text_input("Enter Phone Number")

    if st.button("Login", use_container_width=True):
        for p in st.session_state.patients:
            if p["phone"] == phone:
                st.session_state.current_patient = p
                st.success(f"Welcome back {p['name']} 👋")
                break
        else:
            st.error("Phone number not found")

# ---------------- Auth Check ----------------
if st.session_state.current_patient is None:
    st.stop()

# ---------------- Booking Section ----------------
st.markdown("### 🗓️ Book Appointment")

specializations = list(set(d.specialization for d in st.session_state.doctors))
selected_spec = st.selectbox("Choose Specialization", specializations)

filtered_doctors = [d for d in st.session_state.doctors if d.specialization == selected_spec]
selected_doctor = st.selectbox(
    "Choose Doctor",
    filtered_doctors,
    format_func=lambda d: f"Dr {d.name} | Room {d.room} | {d.price} EGP"
)

selected_day = st.selectbox("Choose Day", list(selected_doctor.schedule.keys()))

available_hours = [
    h for h, s in selected_doctor.schedule[selected_day].items()
    if s == "available"
]

if available_hours:
    selected_hour = st.selectbox("Choose Time", available_hours)

    if st.button("Confirm Booking", use_container_width=True):
        selected_doctor.schedule[selected_day][selected_hour] = "booked"

        appointment = {
            "disease": selected_disease,
            "doctor": selected_doctor.name,
            "patient_name": st.session_state.current_patient["name"],
            "patient_phone": st.session_state.current_patient["phone"],
            "day": selected_day,
            "hour": selected_hour
        }

        st.session_state.current_patient["appointments"].append(appointment)
        st.session_state.appointments.append(appointment)

        st.success("✅ Appointment booked successfully!")
else:
    st.warning("No available times for this day")
