import streamlit as st

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Cure & Go | Doctor Portal",
    page_icon="👨‍⚕️",
    layout="wide"
)

# ---------------------------------------------------------
# 4. Doctor Function
# ---------------------------------------------------------
def doctor_function():
    st.header("👨‍⚕️ Doctor Portal")

    # --- 1. Login Logic ---
    if st.session_state.get('logged_in_doctor') is None:
        st.subheader("Login")
        
        with st.form("doctor_login_form"):
            doc_id_input = st.text_input("Enter Doctor ID (3 digits)", max_chars=3)
            submitted = st.form_submit_button("Login")

            if submitted:
                if len(doc_id_input) == 3 and doc_id_input.isdigit():
                    found_doc = None
                    if 'all_doctors' in st.session_state:
                        for doc in st.session_state['all_doctors']:
                            if doc.doctor_id == doc_id_input:
                                found_doc = doc
                                break
                    
                    if found_doc:
                        st.session_state['logged_in_doctor'] = found_doc
                        st.success(f"Welcome, Dr. {found_doc.name}!")
                        st.experimental_rerun() 
                    else:
                        st.error("Access Denied: Doctor ID not found.")
                else:
                    st.error("Invalid ID format. Must be exactly 3 digits.")
        return 

    # --- 2. Dashboard Logic ---
    current_doc = st.session_state['logged_in_doctor']
    
    with st.sidebar:
        st.title(f"Dr. {current_doc.name}")
        st.write(f"**Specialization:** {current_doc.specialization}")
        st.write("---")
        menu = st.radio("Navigation", ["📅 My Appointments", "⚙️ Manage Availability", "🚪 Logout"])

    # Choice 1 ---> View Own Appointments
    if menu == "📅 My Appointments":
        st.subheader("My Scheduled Appointments")
        all_appointments = st.session_state.get('appointments', [])
        my_appointments = [appt for appt in all_appointments if appt['doctor_id'] == current_doc.doctor_id]

        if my_appointments:
            display_data = []
            for appt in my_appointments:
                display_data.append({
                    "Patient Name": appt['patient_name'],
                    "Phone": appt['patient_phone'],
                    "Day": appt['day'],
                    "Hour": f"{appt['hour']:02d}:00"
                })
            st.table(display_data)
        else:
            st.info("You have no upcoming appointments.")

    # Choice 2 --> Manage Availability
    elif menu == "⚙️ Manage Availability":
        st.subheader("Edit Work Schedule")
        selected_day = st.selectbox("Select Day to Edit", list(current_doc.schedule.keys()))
        st.write(f"**Manage hours for: {selected_day}**")
        st.info("Note: You cannot close hours that are already 'Booked'.")

        col1, col2, col3 = st.columns(3)
        current_schedule = current_doc.schedule[selected_day]
        
        for i in range(24):
            status = current_schedule[i]  # available, not available, booked
            hour_label = f"{i:02d}:00"
            
            if i < 8: col = col1
            elif i < 16: col = col2
            else: col = col3
            
            with col:
                if status == "booked":
                    st.warning(f"🕒 {hour_label}: 🔒 BOOKED")
                else:
                    is_available = (status == "available")
                    btn_label = f"🕒 {hour_label}: {'✅ Open' if is_available else '⛔ Closed'}"
                    btn_key = f"btn_{selected_day}_{i}"
                    
                    if st.button(btn_label, key=btn_key):
                        new_status = "not available" if is_available else "available"
                        current_doc.schedule[selected_day][i] = new_status
                        st.toast(f"Updated {hour_label} to {new_status}")
                        st.experimental_rerun()

    # Choice 3 --> Logout
    elif menu == "🚪 Logout":
        st.session_state['logged_in_doctor'] = None
        st.experimental_rerun()
