import streamlit as st

# -------------------- Hide Streamlit Default Elements --------------------
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

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Cure & Go | Doctor Portal",
    page_icon="👨‍⚕️",
    layout="wide"
)

# -------------------- Custom CSS (محسّن للقراءة) --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    font-family: 'Segoe UI', sans-serif;
    color: #1e293b;  /* لون نص غامق عام */
}

/* العناوين الرئيسية */
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1e293b;
    animation: fadeDown 1s ease;
}
.sub-title {
    text-align: center;
    color: #475569;
    margin-bottom: 35px;
    font-size: 18px;
}

/* الأزرار */
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
    background: linear-gradient(90deg, #1d4ed8, #1e40af);
}

/* تحسين الـ inputs والـ selectbox والـ text area */
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
}

/* خلفية البوكسات الفاتحة */
.css-1d391kg, .stSelectbox > div > div,
.stTextInput > div > div,
.stTextArea > div > div {
    background-color: #ffffff !important;
    border-radius: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* الجداول */
.stDataFrame, .stTable table {
    background-color: white !important;
}
.stTable td, .stTable th {
    color: #1e293b !important;
}

/* الـ sidebar */
section[data-testid="stSidebar"] {
    background-color: #f1f5f9;
    border-right: 1px solid #e2e8f0;
}
.css-1v3fvzy, .css-1d391kg {  /* نصوص الـ sidebar */
    color: #1e293b !important;
}

/* الـ info والـ success والـ error */
.stAlert {
    background-color: white !important;
    color: #1e293b !important;
    border-radius: 10px;
}

/* أزرار إدارة المواعيد (متاح/غير متاح) */
button[kind="secondary"] {
    background-color: #e2e8f0 !important;
    color: #1e293b !important;
}

@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -------------------- Data Class --------------------
class Doctor:
    def __init__(self, doctor_id, name, gender, phone, age, experience, specialization, room, price):
        self.doctor_id = doctor_id
        self.name = name
        self.gender = gender
        self.phone = phone
        self.age = age
        self.experience = experience
        self.specialization = specialization
        self.room = room
        self.price = price
        self.build_schedule()

    def build_schedule(self):
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.schedule = {day: {hour: "available" for hour in range(10, 18)} for day in days}

# -------------------- Initialize Doctors --------------------
if 'all_doctors' not in st.session_state:
    st.session_state['all_doctors'] = [
        Doctor("001", "Haneen El-Barbary", "Female", "01500111111", 27, 2, "Psychotherapy", 1, 250),
        Doctor("002", "Haneen Ayman", "Female", "01000222222", 25, 1, "Pediatrics", 2, 200),
        Doctor("003", "Menna Ayman", "Female", "01000333333", 25, 2, "Dermatology", 3, 300),
        Doctor("004", "Sohaila Gomaa", "Female", "01000444444", 26, 3, "ENT", 4, 220),
        Doctor("005", "Nour Omar", "Female", "01000555555", 27, 3, "Nutrition", 5, 180),
        Doctor("006", "Haneen El Azab", "Female", "01000666666", 25, 1, "Cardiology", 6, 350),
        Doctor("007", "Mostafa Hatem", "Male", "01000777777", 30, 4, "Orthopedics", 7, 300),
        Doctor("008", "Mazen Tarek", "Male", "01000888888", 32, 5, "Neurology", 8, 350),
    ]

if 'appointments' not in st.session_state:
    st.session_state['appointments'] = []

if 'logged_in_doctor' not in st.session_state:
    st.session_state['logged_in_doctor'] = None

# -------------------- Doctor Portal --------------------
def doctor_portal():
    st.markdown("<div class='main-title'>👨‍⚕️ Doctor Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Cure & Go Medical Center</div>", unsafe_allow_html=True)

    # ---------- Login ----------
    if st.session_state['logged_in_doctor'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Doctor Login")
            doc_id_input = st.text_input("Enter Doctor ID (3 digits)", max_chars=3, placeholder="مثال: 001")
            if st.button("Login", use_container_width=True):
                if len(doc_id_input) == 3 and doc_id_input.isdigit():
                    found_doc = next((d for d in st.session_state['all_doctors'] if d.doctor_id == doc_id_input), None)
                    if found_doc:
                        st.session_state['logged_in_doctor'] = found_doc
                        st.success(f"Welcome, Dr. {found_doc.name}! 👋")
                        st.rerun()
                    else:
                        st.error("Doctor ID not found.")
                else:
                    st.error("Invalid ID format. Must be exactly 3 digits.")
        return

    # ---------- Dashboard ----------
    doctor = st.session_state['logged_in_doctor']

    # Sidebar
    with st.sidebar:
        st.title(f"👨‍⚕️ Dr. {doctor.name}")
        st.write(f"**Specialization:** {doctor.specialization}")
        st.write(f"**Room:** {doctor.room}")
        st.markdown("---")
        menu = st.radio("Navigation", ["📅 My Appointments", "⚙️ Manage Availability", "🚪 Logout"])

    # ---------- My Appointments ----------
    if menu == "📅 My Appointments":
        st.subheader("📅 My Scheduled Appointments")
        my_appointments = [a for a in st.session_state['appointments'] if a['doctor_id'] == doctor.doctor_id]
        if my_appointments:
            display_data = [
                {
                    "Patient Name": a['patient_name'],
                    "Phone": a['patient_phone'],
                    "Day": a['day'],
                    "Time": f"{a['hour']}:00"
                }
                for a in my_appointments
            ]
            st.table(display_data)
        else:
            st.info("You have no upcoming appointments yet.")

    # ---------- Manage Availability ----------
    elif menu == "⚙️ Manage Availability":
        st.subheader("⚙️ Manage Work Schedule")
        selected_day = st.selectbox("Select Day to Edit", list(doctor.schedule.keys()))

        st.markdown(f"**{selected_day}** – Click to toggle availability (10:00 to 17:00)")
        col1, col2, col3 = st.columns(3)

        for i in range(10, 18):
            status = doctor.schedule[selected_day][i]
            btn_label = f"{i}:00 - {'✅ Available' if status == 'available' else '⛔ Not Available'}"
            col = col1 if i < 13 else col2 if i < 15 else col3
            with col:
                if st.button(btn_label, key=f"{selected_day}_{i}", use_container_width=True):
                    new_status = "available" if status == "not available" else "not available"
                    doctor.schedule[selected_day][i] = new_status
                    st.success(f"{i}:00 updated to **{new_status}**")
                    st.rerun()

    # ---------- Logout ----------
    elif menu == "🚪 Logout":
        st.session_state['logged_in_doctor'] = None
        st.rerun()

# -------------------- Main --------------------
def main():
    doctor_portal()

if __name__ == "__main__":
    main()
