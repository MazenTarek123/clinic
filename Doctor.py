import streamlit as st

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
    st.header("👨‍⚕️ Doctor Portal")

    # ---------- Login ----------
    if st.session_state['logged_in_doctor'] is None:
        st.subheader("Login")
        doc_id_input = st.text_input("Enter Doctor ID (3 digits)", max_chars=3)
        if st.button("Login"):
            if len(doc_id_input) == 3 and doc_id_input.isdigit():
                found_doc = next((d for d in st.session_state['all_doctors'] if d.doctor_id == doc_id_input), None)
                if found_doc:
                    st.session_state['logged_in_doctor'] = found_doc
                    st.success(f"Welcome, Dr. {found_doc.name}!")
                    st.rerun()
                else:
                    st.error("Doctor ID not found.")
            else:
                st.error("Invalid ID format. Must be exactly 3 digits.")
        return

    # ---------- Dashboard ----------
    doctor = st.session_state['logged_in_doctor']
    with st.sidebar:
        st.title(f"Dr. {doctor.name}")
        st.write(f"**Specialization:** {doctor.specialization}")
        menu = st.radio("Navigation", ["📅 My Appointments", "⚙️ Manage Availability", "🚪 Logout"])

    # ---------- My Appointments ----------
    if menu == "📅 My Appointments":
        st.subheader("My Scheduled Appointments")
        my_appointments = [a for a in st.session_state['appointments'] if a['doctor_id'] == doctor.doctor_id]
        if my_appointments:
            display_data = [{"Patient Name": a['patient_name'], "Phone": a['patient_phone'], "Day": a['day'], "Hour": f"{a['hour']}:00"} for a in my_appointments]
            st.table(display_data)
        else:
            st.info("You have no upcoming appointments.")

    # ---------- Manage Availability ----------
    elif menu == "⚙️ Manage Availability":
        st.subheader("Edit Work Schedule")
        selected_day = st.selectbox("Select Day to Edit", list(doctor.schedule.keys()))
        col1, col2, col3 = st.columns(3)
        for i in range(10, 18):
            status = doctor.schedule[selected_day][i]
            btn_label = f"{i}:00 - {'✅ Open' if status=='available' else '⛔ Closed'}"
            col = col1 if i < 14 else col2 if i < 16 else col3
            with col:
                if st.button(btn_label, key=f"{selected_day}_{i}"):
                    doctor.schedule[selected_day][i] = "available" if status=="not available" else "not available"
                    st.toast(f"Updated {i}:00 to {doctor.schedule[selected_day][i]}")
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
