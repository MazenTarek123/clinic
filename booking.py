import streamlit as st

# إخفاء header, footer, menu
st.markdown("""
<style>
    /* إخفاء عناصر Streamlit */
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    footer {display: none !important;}
    .block-container {padding-top: 3rem !important;}
    
    /* خلفية عامة */
    .stApp {
        background: linear-gradient(to bottom, #f0f9ff, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* عنوان المرض */
    .disease-tag {
        text-align: center;
        background: #2563eb;
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 28px;
        font-weight: bold;
        margin: 30px auto;
        max-width: 80%;
    }
    
    /* عناوين */
    h1, h2, h3 {
        color: #1e40af;
        text-align: center;
        font-weight: bold;
    }
    
    /* Radio buttons */
    div.row-widget.stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 3rem;
    }
    div.row-widget.stRadio > div > label {
        background: #2563eb;
        color: white;
        padding: 10px 30px;
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Inputs و Selectbox */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #2563eb;
        padding: 12px;
        font-size: 16px;
    }
    
    /* Labels */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label {
        font-weight: bold;
        color: #1e40af;
        font-size: 18px;
    }
    
    /* Buttons */
    .stButton > button {
        background: #2563eb;
        color: white;
        font-size: 20px;
        height: 60px;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        width: 100%;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background: #1d4ed8;
    }
    
    /* Success/Error/Warning */
    .stSuccess, .stError, .stWarning {
        text-align: center;
        font-size: 20px;
        border-radius: 12px;
        padding: 15px;
    }
    
    /* Table */
    .stTable {
        margin: 0 auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Cure & Go | Patient Portal", page_icon="🧑‍🦱", layout="centered")

# جلب اسم المرض
query_params = st.query_params
selected_disease = query_params.get("disease", ["General Consultation"])[0]

st.markdown(f"<div class='disease-tag'>Patient Portal - {selected_disease}</div>", unsafe_allow_html=True)

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

# دكاترة افتراضية (نفس بياناتك)
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
st.markdown("<h2>🧑‍🦱 Patient Portal</h2>", unsafe_allow_html=True)

option = st.radio("Do you want to Login or Create a New Account?", ["Login", "Create Account"], horizontal=True)

if option == "Create Account":
    st.markdown("<h3>Create New Account</h3>", unsafe_allow_html=True)
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
            st.rerun()
        else:
            st.error("Please fill name and phone number")

elif option == "Login":
    st.markdown("<h3>Login to Your Account</h3>", unsafe_allow_html=True)
    phone = st.text_input("Enter your phone number to login")
    if st.button("Login"):
        found = False
        for patient in st.session_state.patients:
            if patient["phone"] == phone:
                st.session_state.current_patient = patient
                st.success(f"Welcome back, {patient['name']}!")
                found = True
                st.rerun()
                break
        if not found:
            st.error("Phone number not found. Please create an account.")

# ------------- Check if logged in -------------
if st.session_state.current_patient is None:
    st.warning("Please login or create an account first.")
    st.stop()

st.success(f"Welcome {st.session_state.current_patient['name']}!")

# ----------------- Booking --------------------
st.markdown("<h3>Book New Appointment</h3>", unsafe_allow_html=True)

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
        st.success(f"Appointment booked successfully for {selected_disease} with Dr {selected_doctor.name} on {selected_day} at {selected_hour}:00")
        st.balloons()
else:
    st.warning("No available hours for this doctor on this day. Please choose another day or doctor.")

# ------------- View & Cancel Appointments -------------
appointments = st.session_state.current_patient["appointments"]
if appointments:
    st.markdown("<h3>📋 Your Appointments</h3>", unsafe_allow_html=True)
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

    st.markdown("<h3>❌ Cancel an Appointment</h3>", unsafe_allow_html=True)
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
        st.rerun()
else:
    st.info("You have no appointments yet.")
