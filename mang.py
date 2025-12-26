import streamlit as st

# =========================
# Data Class
# =========================
class Doctor:
    def __init__(self, doctor_id, name, gender, phone, age, exp, spec, room, price):
        self.doctor_id = doctor_id
        self.name = name
        self.gender = gender
        self.phone = phone
        self.age = age
        self.experience = exp
        self.specialization = spec
        self.room = room
        self.price = price

# =========================
# Session State
# =========================
if "manager_logged_in" not in st.session_state:
    st.session_state.manager_logged_in = False

if "doctors" not in st.session_state:
    st.session_state.doctors = [
        Doctor("001", "Haneen El-Barbary", "Female", "01500111111", 27, 2, "Psychotherapy", 1, 250),
        Doctor("002", "Mostafa Hatem", "Male", "01000777777", 30, 4, "Orthopedics", 2, 300),
    ]

# =========================
# Manager Login
# =========================
def manager_login():
    st.subheader("🔒 Manager Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "12345":
            st.session_state.manager_logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Wrong credentials")

# =========================
# Manager Dashboard
# =========================
def manager_dashboard():
    st.title("🛠 Manager Dashboard")

    if st.sidebar.button("Logout"):
        st.session_state.manager_logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["📋 Doctors", "➕ Add Doctor", "❌ Delete Doctor"])

    # View Doctors
    with tab1:
        data = [{
            "ID": d.doctor_id,
            "Name": d.name,
            "Specialization": d.specialization,
            "Room": d.room,
            "Price": d.price
        } for d in st.session_state.doctors]

        st.table(data)

    # Add Doctor
    with tab2:
        with st.form("add_doc"):
            name = st.text_input("Name")
            gender = st.selectbox("Gender", ["Male", "Female"])
            phone = st.text_input("Phone")
            age = st.number_input("Age", min_value=25, max_value=60)
            spec = st.text_input("Specialization")
            price = st.number_input("Price", min_value=100, max_value=350)
            submit = st.form_submit_button("Add")

            if submit:
                new_id = f"{len(st.session_state.doctors)+1:03d}"
                st.session_state.doctors.append(
                    Doctor(new_id, name, gender, phone, age, 1, spec, len(st.session_state.doctors)+1, price)
                )
                st.success("Doctor Added")
                st.rerun()

    # Delete Doctor
    with tab3:
        ids = [d.doctor_id for d in st.session_state.doctors]
        selected = st.selectbox("Select Doctor ID", ids)
        if st.button("Delete"):
            st.session_state.doctors = [d for d in st.session_state.doctors if d.doctor_id != selected]
            st.success("Doctor Deleted")
            st.rerun()

# =========================
# Main
# =========================
if not st.session_state.manager_logged_in:
    manager_login()
else:
    manager_dashboard()
