import streamlit as st

# إخفاء عناصر Streamlit
st.markdown("""
<style>
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Cure & Go | Booking", page_icon="📅", layout="centered")

# CSS لستايل زي موقعك (أزرق، خطوط نظيفة)
st.markdown("""
<style>
    .stApp {background: linear-gradient(to bottom, #f0f9ff, #ffffff);}
    h1 {color: #1e40af; text-align: center;}
    .disease-tag {text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 10px; font-size: 22px; margin: 20px 0;}
    .stButton>button {background: #2563eb; color: white; font-size: 18px; height: 50px; border-radius: 10px;}
    .stSuccess {text-align: center; font-size: 20px;}
</style>
""", unsafe_allow_html=True)

# جلب اسم المرض من URL
query_params = st.query_params
selected_disease = query_params.get("disease", ["General"])[0]

st.markdown(f"<div class='disease-tag'>Booking for {selected_disease}</div>", unsafe_allow_html=True)

# تهيئة البيانات
if "doctors" not in st.session_state:
    st.session_state.doctors = []
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "patients" not in st.session_state:
    st.session_state.patients = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# لو مفيش دكاترة
if not st.session_state.doctors:
    st.error("No doctors available.")
    st.stop()

# ---------- Login or Create Account ----------
option = st.radio("Do you want to Login or Create a New Account?", ["Login", "Create Account"], horizontal=True)

if option == "Create Account":
    st.markdown("### Create New Account")
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
    st.markdown("### Login to Your Account")
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
st.markdown("### Book New Appointment")

specializations = list(set(doc.specialization for doc in st.session_state.doctors))
selected_specialization = st.selectbox("Choose a specialization", specializations)

available_doctors = [doc for doc in st.session_state.doctors if doc.specialization == selected_specialization]
selected_doctor = st.selectbox("Choose a doctor", available_doctors, format_func=lambda d: f"Dr {d.name}")

# جدول مواعيد افتراضي لو مش موجود
if not hasattr(selected_doctor, "schedule"):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = ["09", "10", "11", "12", "14", "15", "16", "17"]
    selected_doctor.schedule = {day: {hour: "available" for hour in hours} for day in days}

available_days = list(selected_doctor.schedule.keys())
selected_day = st.selectbox("Choose a day", available_days)

available_hours = [hour for hour, status in selected_doctor.schedule[selected_day].items() if status == "available"]

if available_hours:
    selected_hour = st.selectbox("Choose an appointment time", available_hours)
    if st.button("Book Appointment"):
        selected_doctor.schedule[selected_day][selected_hour] = "booked"
        appointment = {
            "disease": selected_disease,  # اسم المرض اللي جاء من URL
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
    st.markdown("### 📋 Your Appointments")
    display_apps = []
    for i, app in enumerate(appointments, start=1):
        display_apps.append({
            "No.": i,
            "Disease": app.get("disease", "N/A"),
            "Doctor": f"Dr {app['doctor']}",
            "Day": app['day'],
            "Time": f"{app['hour']}:00"
        })
    st.table(display_apps)

    st.markdown("### ❌ Cancel an Appointment")
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