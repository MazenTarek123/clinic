import streamlit as st

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Cure & Go | Patient Portal",
    page_icon="🧑‍🦱",
    layout="wide"
)

# ---------------- Hide Streamlit UI ----------------
st.markdown("""
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Custom Style ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    font-family: 'Segoe UI', sans-serif;
}

/* Titles */
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f2937;
}

.sub-title {
    text-align: center;
    color: #374151;
    margin-bottom: 35px;
    font-size: 18px;
}

/* Buttons */
.stButton > button {
    border-radius: 14px;
    padding: 12px;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* Text colors (SMART FIX) */
p, label, h1, h2, h3, h4 {
    color: #1f2937 !important;
}

/* Inputs text */
input, textarea {
    color: #111827 !important;
}

/* Selectbox text */
div[data-baseweb="select"] span {
    color: #111827 !important;
}

/* Selectbox shape */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px;
    border: 1px solid #d1d5db;
}

/* Radio buttons */
.stRadio label {
    color: #1f2937 !important;
    font-weight: 600;
}

/* Tables */
table, th, td {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Get Disease From URL (FIXED) ----------------
query_params = st.query_params
selected_disease = query_params.get("disease", "General Consultation")
if isinstance(selected_disease, list):
    selected_disease = selected_disease[0]

# ---------------- Header ----------------
st.markdown("<div class='main-title'>🧑‍🦱 Patient Portal</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='sub-title'>📌 Booking for <b>{selected_disease}</b></div>",
    unsafe_allow_html=True
)

# ---------------- Session State ----------------
if "doctors" not in st.session_state:
    st.session_state.doctors = []
if "patients" not in st.session_state:
    st.session_state.patients = []
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# ---------------- Doctor Class ----------------
class Doctor:
    def __init__(self, doctor_id, name, gender, phone, age, exp, specialization, room, price):
        self.doctor_id = doctor_id
        self.name = name
        self.gender = gender
        self.phone = phone
        self.age = age
        self.exp = exp
        self.specialization = specialization
        self.room = room
        self.price = price

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = ["09", "10", "11", "12", "14", "15", "16", "17"]
        self.schedule = {day: {hour: "available" for hour in hours} for day in days}

# ---------------- Dummy Doctors ----------------
if not st.session_state.doctors:
    st.session_state.doctors = [
        Doctor("001", "Haneen El-Barbary", "Female", "01500111111", 27, 2, "Psychotherapy", 1, 250),
        Doctor("002", "Haneen Ayman", "Female", "01000222222", 25, 1, "Pediatrics", 2, 200),
        Doctor("003", "Menna Ayman", "Female", "01000333333", 25, 2, "Dermatology", 3, 300),
        Doctor("004", "Sohaila Gomaa", "Female", "01000444444", 26, 3, "ENT", 4, 220),
        Doctor("005", "Nour Omar", "Female", "01000555555", 27, 3, "Nutrition", 5, 180),
        Doctor("006", "Haneen El Azab", "Female", "01000666666", 25, 1, "Cardiology", 6, 350),
        Doctor("007", "Mostafa Hatem", "Male", "01000777777", 30, 4, "Orthopedics", 7, 300),
        Doctor("008", "Mazen Tarek", "Male", "01000888888", 32, 5, "Neurology", 8, 350),
    ]

# ---------------- Login / Register ----------------
option = st.radio("Do you want to Login or Create a New Account?", ["Login", "Create Account"])

if option == "Create Account":
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1, step=1)
    phone_number = st.text_input("Enter your phone number")

    if st.button("Create Account"):
        if name and phone_number:
            patient = {
                "name": name,
                "age": age,
                "phone": phone_number,
                "appointments": []
            }
            st.session_state.patients.append(patient)
            st.session_state.current_patient = patient
            st.success(f"Account created successfully! Welcome {name}")

if option == "Login":
    phone = st.text_input("Enter your phone number to login")

    if st.button("Login"):
        for patient in st.session_state.patients:
            if patient["phone"] == phone:
                st.session_state.current_patient = patient
                st.success(f"Welcome back, {patient['name']}!")
                break
        else:
            st.error("Phone number not found. Please create an account.")

# ---------------- Auth Check ----------------
if st.session_state.current_patient is None:
    st.warning("Please login or create an account first.")
    st.stop()

st.success(f"Welcome {st.session_state.current_patient['name']}")

# ---------------- Booking ----------------
specializations = list(set(doc.specialization for doc in st.session_state.doctors))
selected_specialization = st.selectbox("Choose a specialization", specializations)

available_doctors = [doc for doc in st.session_state.doctors if doc.specialization == selected_specialization]
selected_doctor = st.selectbox("Choose a doctor", available_doctors, format_func=lambda d: f"Dr {d.name}")

selected_day = st.selectbox("Choose a day", list(selected_doctor.schedule.keys()))

available_hours = [
    hour for hour, status in selected_doctor.schedule[selected_day].items()
    if status == "available"
]

if available_hours:
    selected_hour = st.selectbox("Choose an appointment time", available_hours)

    if st.button("Book Appointment"):
        selected_doctor.schedule[selected_day][selected_hour] = "booked"

        appointment = {
            "disease": selected_disease,
            "doctor": selected_doctor.name,
            "day": selected_day,
            "hour": selected_hour
        }

        st.session_state.current_patient["appointments"].append(appointment)
        st.session_state.appointments.append(appointment)

        st.success(
            f"Appointment booked successfully with Dr {selected_doctor.name} "
            f"on {selected_day} at {selected_hour}:00"
        )
else:
    st.warning("No available hours for this doctor on this day.")

# ---------------- View Appointments ----------------
appointments = st.session_state.current_patient["appointments"]

if appointments:
    st.subheader("📋 Your Appointments")
    st.table([
        {
            "Disease": app["disease"],
            "Doctor": f"Dr {app['doctor']}",
            "Day": app["day"],
            "Time": f"{app['hour']}:00"
        }
        for app in appointments
    ])
else:
    st.info("You have no appointments yet.")
