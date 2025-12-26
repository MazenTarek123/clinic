import streamlit as st

# إخفاء header, footer, menu
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

st.set_page_config(
    page_title="Cure & Go | Patient Portal",
    page_icon="🧑‍🦱",
    layout="wide"
)

# نفس الستايل بتاع الـ Admin بالظبط
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
@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# جلب اسم المرض من URL
query_params = st.query_params
selected_disease = query_params.get("disease", ["General Consultation"])[0]

st.markdown("<div class='main-title'>🧑‍🦱 Patient Portal</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Booking for {selected_disease}</div>", unsafe_allow_html=True)

# تهيئة البيانات
if "doctors" not in st.session_state:
    st.session_state.doctors = []
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "patients" not in st.session_state:
    st.session_state.patients = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# تعريف Doctor class
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

# دكاترة افتراضية
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

# ---------- Login or Create Account ----------
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
        found = False
        for patient in st.session_state.patients:
            if patient["phone"] == phone:
                st.session_state.current_patient = patient
                st.success(f"Welcome back, {patient['name']}!")
                found = True
                break
        if not found:
            st.error("Phone number not found. Please create an account.")

# ------------- check if logged in -------------
if st.session_state.current_patient is None:
    st.warning("Please login or create an account first.")
    st.stop()
else:
    st.success(f"Welcome {st.session_state.current_patient['name']}")

#----------------- booking --------------------
specializations = list(set(doc.specialization for doc in st.session_state.doctors))
selected_specialization = st.selectbox("Choose a specialization", specializations)

available_doctors = [doc for doc in st.session_state.doctors if doc.specialization == selected_specialization]
selected_doctor = st.selectbox("Choose a doctor", available_doctors, format_func=lambda d: f"Dr {d.name}")

available_days = list(selected_doctor.schedule.keys())
selected_day = st.selectbox("Choose a day", available_days)

available_hours = [hour for hour, status in selected_doctor.schedule[selected_day].items() if status == "available"]

if available_hours:
    selected_hour = st.selectbox("Choose an appointment time", available_hours)
    if st.button("Book Appointment"):
        selected_doctor.schedule[selected_day][selected_hour] = "booked"
        appointment = {
            "disease": selected_disease,
            "doctor_id": selected_doctor.doctor_id,
            "doctor": selected_doctor.name,
            "patient_name": st.session_state.current_patient["name"],
            "patient_phone": st.session_state.current_patient["phone"],
            "day": selected_day,
            "hour": selected_hour
        }
        st.session_state.current_patient["appointments"].append(appointment)
        st.session_state.appointments.append(appointment)
        st.success(f"Appointment booked successfully with Dr {selected_doctor.name} on {selected_day} at {selected_hour}:00")
else:
    st.warning("No available hours for this doctor on this day. Please choose another day or doctor.")

#------------- view & cancel appointments -------------
appointments = st.session_state.current_patient["appointments"]
if appointments:
    st.subheader("📋 Your Appointments")
    display_apps = []
    for i, app in enumerate(appointments, start=1):
        display_apps.append({
            "No.": i,
            "Disease": app.get("disease", "N/A"),
            "Doctor": f"Dr {app['doctor']}",
            "Day": app["day"],
            "Time": f"{app['hour']}:00"
        })
    st.table(display_apps)
    st.markdown("---")
    st.subheader("❌ Cancel an Appointment")
    cancel_options = [f"Dr {app['doctor']} at {app['hour']}:00 on {app['day']}" for app in appointments]
    appointment_to_cancel = st.selectbox("Select an appointment to cancel", cancel_options)
    if st.button("Cancel Appointment"):
        index_to_cancel = cancel_options.index(appointment_to_cancel)
        canceled_app = appointments.pop(index_to_cancel)
        st.session_state.appointments = [
            a for a in st.session_state.appointments
            if not (a['doctor'] == canceled_app['doctor'] and a['day'] == canceled_app['day'] and a['hour'] == canceled_app['hour'])
        ]
        for doc in st.session_state.doctors:
            if doc.name == canceled_app["doctor"]:
                doc.schedule[canceled_app["day"]][canceled_app["hour"]] = "available"
                break
        st.success("Appointment canceled successfully.")
else:
    st.info("You have no appointments yet.")
