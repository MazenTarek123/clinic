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
header, footer, #MainMenu {visibility: hidden;}
.block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2f7, #dbe4f3);
    font-family: 'Segoe UI', sans-serif;
}

/* Center Card */
.card {
    background: #ffffff;
    padding: 40px;
    border-radius: 20px;
    max-width: 850px;
    margin: auto;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

/* Titles */
.main-title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    color: #1f2937;
}

.sub-title {
    text-align: center;
    color: #4b5563;
    margin-bottom: 30px;
    font-size: 17px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 14px;
    padding: 12px;
    border: none;
    font-weight: 600;
}

/* Inputs & Selects */
input, textarea, div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #d1d5db !important;
}

/* Radio */
.stRadio label {
    color: #1f2937 !important;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🧑‍🦱 Patient Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>📌 Book your appointment easily</div>", unsafe_allow_html=True)

# ---------------- CARD START ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

# ---------------- Session ----------------
if "patients" not in st.session_state:
    st.session_state.patients = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# ---------------- LOGIN / REGISTER ----------------
option = st.radio(
    "Do you want to Login or Create a New Account?",
    ["Login", "Create Account"]
)

if option == "Create Account":
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1)
    phone = st.text_input("Phone Number")

    if st.button("Create Account"):
        st.session_state.current_patient = {
            "name": name,
            "age": age,
            "phone": phone,
            "appointments": []
        }
        st.success("Account created successfully!")

else:
    phone = st.text_input("Enter your phone number")

    if st.button("Login"):
        st.session_state.current_patient = {
            "name": "Patient",
            "phone": phone,
            "appointments": []
        }
        st.success("Logged in successfully!")

# ---------------- AUTH CHECK ----------------
if st.session_state.current_patient:
    st.divider()
    st.subheader("📅 Book Appointment")

    specialization = st.selectbox(
        "Specialization",
        ["ENT", "Dermatology", "Cardiology", "Neurology"]
    )

    doctor = st.selectbox(
        "Doctor",
        ["Dr Ahmed", "Dr Sara", "Dr Mohamed"]
    )

    day = st.selectbox(
        "Day",
        ["Monday", "Tuesday", "Wednesday"]
    )

    time = st.selectbox(
        "Time",
        ["10:00", "11:00", "12:00"]
    )

    if st.button("Confirm Booking"):
        st.success("✅ Appointment booked successfully!")

st.markdown("</div>", unsafe_allow_html=True)
# ---------------- CARD END ----------------
