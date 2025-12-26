import streamlit as st

# -------------------- Custom CSS (Colors Inverted) --------------------
st.set_page_config(page_title="Cure & Go | Doctor", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.stApp {
    background: #f5f7fa; /* Background فاتح */
    font-family: 'Segoe UI', sans-serif;
    color: #1f2937; /* النص داكن */
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f2937; /* عنوان داكن */
    animation: fadeDown 1s ease;
}
.sub-title {
    text-align: center;
    color: #374151; /* عنوان فرعي داكن */
    margin-bottom: 35px;
}
.stButton>button {
    border-radius: 14px;
    padding: 12px;
    background: #1d4ed8; /* أزرق غامق */
    color: white; /* النص أبيض على الزر الغامق */
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.06);
    background: #2563eb; /* تدرج عند hover */
}
.stSelectbox>div>div>div {
    background-color: #e0e7ff !important; /* بوكس فاتح للاختيارات */
    color: #1f2937 !important;
}
.stTextInput>div>div>input {
    background-color: #e0e7ff !important; /* Input فاتح */
    color: #1f2937 !important;
}
.stNumberInput>div>div>input {
    background-color: #e0e7ff !important; 
    color: #1f2937 !important;
}
.stTable td, .stTable th {
    color: #1f2937; /* نص الجدول داكن */
}
@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------- Doctor Data Class --------------------
class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        # جدول المواعيد: كل يوم 24 ساعة، البداية "متاح" من 10 إلى 17، الباقي "غير متاح"
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.schedule = {day: {hour: "not available" for hour in range(24)} for day in days}
        for day in self.schedule:
            for hour in range(10, 18):
                self.schedule[day][hour] = "available"

# -------------------- Session State Initialization --------------------
if 'all_doctors' not in st.session_state:
    st.session_state['all_doctors'] = [
        Doctor("001", "Haneen El-Barbary", "Psychotherapy"),
        Doctor("002", "Haneen Ayman", "Pediatrics"),
        Doctor("003", "Menna Ayman", "Dermatology"),
        Doctor("004", "Sohaila Gomaa", "ENT"),
        Doctor("005", "Nour Omar", "Nutrition"),
        Doctor("006", "Haneen El Azab", "Cardiology"),
        Doctor("007", "Mostafa Hatem", "Orthopedics"),
        Doctor("008", "Mazen Tarek", "Neurology"),
    ]

if 'logged_in_doctor' not in st.session_state:
    st.session_state['logged_in_doctor'] = None
if 'appointments' not in st.session_state:
    st.session_state['appointments'] = []

# -------------------- Doctor Function --------------------
def doctor_portal():
    st.markdown("<div class='main-title'>Doctor Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Cure & Go Clinic</div>", unsafe_allow_html=True)

    # --- Login ---
    if st.session_state['logged_in_doctor'] is None:
        st.subheader("Login")
        with st.form("doctor_login"):
            doc_id = st.text_input("Enter your Doctor ID (3 digits)", max_chars=3)
            submitted = st.form_submit_button("Login")
            if submitted:
                found = next((d for d in st.session_state['all_doctors'] if d.doctor_id == doc_id), None)
                if found:
                    st.session_state['logged_in_doctor'] = found
                    st.success(f"Welcome, Dr. {found.name}!")
                    st.rerun()
                else:
                    st.error("Doctor ID not found.")
        return

    doctor = st.session_state['logged_in_doctor']

    # Sidebar
    with st.sidebar:
        st.title(f"Dr. {doctor.name}")
        st.write(f"**Specialization:** {doctor.specialization}")
        menu = st.radio("Navigation", ["📅 My Appointments", "⚙️ Manage Availability", "🚪 Logout"])

    # --- My Appointments ---
    if menu == "📅 My Appointments":
        st.subheader("My Scheduled Appointments")
        my_apps = [a for a in st.session_state['appointments'] if a['doctor_id'] == doctor.doctor_id]
        if my_apps:
            st.table([{
                "Patient Name": a['patient_name'],
                "Phone": a['patient_phone'],
                "Day": a['day'],
                "Hour": f"{a['hour']}:00"
            } for a in my_apps])
        else:
            st.info("You have no upcoming appointments.")

    # --- Manage Availability ---
    elif menu == "⚙️ Manage Availability":
        st.subheader("Edit Work Schedule")
        day = st.selectbox("Select Day", list(doctor.schedule.keys()))
        col1, col2, col3 = st.columns(3)
        for i in range(24):
            status = doctor.schedule[day][i]
            hour_label = f"{i:02d}:00"
            if i < 8: col = col1
            elif i < 16: col = col2
            else: col = col3

            with col:
                if status == "booked":
                    st.warning(f"🕒 {hour_label}: 🔒 BOOKED")
                else:
                    btn_label = f"🕒 {hour_label}: {'✅ Open' if status=='available' else '⛔ Closed'}"
                    if st.button(btn_label, key=f"{day}_{i}"):
                        doctor.schedule[day][i] = "not available" if status=="available" else "available"
                        st.toast(f"{hour_label} updated")
                        st.rerun()

    # --- Logout ---
    elif menu == "🚪 Logout":
        st.session_state['logged_in_doctor'] = None
        st.rerun()

# -------------------- Main --------------------
def main():
    doctor_portal()

if __name__ == "__main__":
    main()
