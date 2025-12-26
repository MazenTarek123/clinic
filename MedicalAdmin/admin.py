import streamlit as st


# ======================================================
# Streamlit (Header + Menu + Footer + Hamburger)
# ======================================================
hide_streamlit_elements = """
<style>
    
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    section[data-testid="stSidebar"] > div:first-child {visibility: hidden !important;}
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

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="Cure & Go | Admin",
    page_icon="🛠️",
    layout="wide"
)

# ======================================================
# CSS (شيلنا كل حاجة متعلقة بالـ card والأنيميشن)
# ======================================================
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
    animation: fadeDown 1s ease;
}
.sub-title {
    text-align: center;
    color: #374151;
    margin-bottom: 35px;
}

/* Buttons */
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

/* Animation للعنوان الرئيسي بس */
@keyframes fadeDown {
    from {opacity:0; transform:translateY(-30px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# Doctor Class & Data & Login (بدون تغيير)
# ======================================================
class Doctor:
    def __init__(self, doctor_id, name, gender, phone, age, exp, spec, room, price):
        self.doctor_id = doctor_id
        self.name = name
        self.gender = gender
        self.phone = phone
        self.age = age
        self.exp = exp
        self.specialization = spec
        self.room = room
        self.price = price

if "doctors" not in st.session_state:
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

if "manager_logged" not in st.session_state:
    st.session_state.manager_logged = False

def manager_login():
    st.markdown("<div class='main-title'>Admin Login</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Cure & Go Medical Center</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "12345":
                st.session_state.manager_logged = True
                st.success("Welcome Admin 👋")
                st.rerun()
            else:
                st.error("Wrong username or password")

# ======================================================
# Dashboard (بدون أي card أبيض)
# ======================================================
def manager_dashboard():
    st.markdown("<div class='main-title'>🛠 Admin Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Manage Doctors & Clinic System</div>", unsafe_allow_html=True)

    # Sidebar بدون صورة
    st.sidebar.title("🏥 Cure & Go Clinic")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.manager_logged = False
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "👨‍⚕️ Doctors",
        "➕ Add Doctor",
        "❌ Delete Doctor",
        "📊 Statistics"
    ])

    # Tab 1: Doctors - مباشرة بدون card
    with tab1:
        doctors_data = [{
            "ID": d.doctor_id,
            "Name": d.name,
            "Gender": d.gender,
            "Phone": d.phone,
            "Age": d.age,
            "Experience": d.exp,
            "Specialization": d.specialization,
            "Room": d.room,
            "Price": d.price
        } for d in st.session_state.doctors]

        st.table(doctors_data)

    # Tab 2: Add Doctor - مباشرة بدون card
    with tab2:
        with st.form("add_doctor"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Doctor Name")
                gender = st.selectbox("Gender", ["Male", "Female"])
                phone = st.text_input("Phone")
                age = st.number_input("Age", min_value=25, max_value=60)

            with col2:
                specialization = st.text_input("Specialization")
                exp = st.number_input("Experience (Years)", min_value=0)
                price = st.number_input("Price", min_value=100, max_value=350)

            new_id = f"{len(st.session_state.doctors)+1:03d}"
            new_room = len(st.session_state.doctors) + 1
            st.info(f"Doctor ID: {new_id} | Room: {new_room}")

            if st.form_submit_button("Add Doctor"):
                st.session_state.doctors.append(
                    Doctor(new_id, name, gender, phone, age, exp, specialization, new_room, price)
                )
                st.success("Doctor Added Successfully")
                st.rerun()

    # Tab 3: Delete Doctor - مباشرة بدون card
    with tab3:
        options = [f"{d.doctor_id} - {d.name}" for d in st.session_state.doctors]
        selected = st.selectbox("Select Doctor", options)

        if st.button("Delete Doctor"):
            selected_id = selected.split(" - ")[0]
            st.session_state.doctors = [
                d for d in st.session_state.doctors if d.doctor_id != selected_id
            ]
            st.success("Doctor Deleted Successfully")
            st.rerun()

    # Tab 4: Statistics - مباشرة بدون card
    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Doctors", len(st.session_state.doctors))
        with col2:
            st.metric("Total Rooms", max(d.room for d in st.session_state.doctors) if st.session_state.doctors else 0)

        spec_count = {}
        for d in st.session_state.doctors:
            spec_count[d.specialization] = spec_count.get(d.specialization, 0) + 1

        st.bar_chart(spec_count)

# ======================================================
# Main
# ======================================================
def main():
    if not st.session_state.manager_logged:
        manager_login()
    else:
        manager_dashboard()

if __name__ == "__main__":
    main()
