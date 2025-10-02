import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Max Hall Solutions Load Intake", layout="wide")

# ---------------------- THEME / CSS ----------------------
st.markdown(
    """
    <style>
    .stApp {
        background: 
            linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
            url("https://raw.githubusercontent.com/travis93451/SoloAppProjects/main/assets/abstract_bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }

    :root {
      --mh-bg: #FFFFFF; /* White input background */
      --mh-fg: #000000; /* Black text for visibility */
      --mh-border: #FFD700;
      --mh-border-focus: #FFEA00;
      --mh-radius: 5px;
      --mh-shadow: 0 4px 8px rgba(0,0,0,.3);
      --mh-placeholder: #666666;
    }

    input::placeholder, textarea::placeholder {
      color: var(--mh-placeholder);
      opacity: 1;
    }

    /* Title styling */
    .app-title {
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 0 0 10px #FFD700, 0 0 20px #FFEA00, 0 0 30px #FFEA00;
        animation: titleGlow 2s infinite alternate;
    }

    @keyframes titleGlow {
        0%   { text-shadow: 0 0 10px #FFD700, 0 0 20px #FFEA00; }
        50%  { text-shadow: 0 0 20px #FFD700, 0 0 40px #FFEA00, 0 0 60px #FFEA00; }
        100% { text-shadow: 0 0 10px #FFD700, 0 0 20px #FFEA00; }
    }

    /* Inputs unified */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input,
    [data-testid="stTextArea"] textarea {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
      animation: breathingGlow 3s infinite ease-in-out;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus,
    [data-testid="stTimeInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
      border-color: var(--mh-border-focus);
      box-shadow: 0 0 15px var(--mh-border-focus);
      animation: pulseGlow 0.6s ease;
    }

    /* Number spinner buttons */
    [data-testid="stNumberInput"] button {
      background-color: #1a1a2e !important;
      color: #FFD700 !important;
      border: 1px solid var(--mh-border);
      border-radius: 4px;
      transition: all 0.3s ease;
    }
    [data-testid="stNumberInput"] button:hover {
      background-color: #FFD700 !important;
      color: #1a1a2e !important;
      box-shadow: 0 0 10px #FFD700;
      transform: scale(1.1);
    }

    /* Selectboxes & TimePickers */
    [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stTimeInput"] div[data-baseweb="select"] {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
      transition: all 0.3s ease;
      animation: breathingGlow 3s infinite ease-in-out;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within,
    [data-testid="stTimeInput"] div[data-baseweb="select"]:focus-within {
      border-color: var(--mh-border-focus);
      box-shadow: 0 0 15px var(--mh-border-focus);
      animation: pulseGlow 0.6s ease;
    }

    /* Dropdown menu items */
    [data-baseweb="select"] li {
      background-color: #FFFFFF !important;
      color: #000000 !important;
      opacity: 0;
      transform: translateY(-10px);
      animation: dropdownFade 0.25s ease forwards;
    }
    [data-baseweb="select"] li:hover {
      background-color: #FFD700 !important;
      color: #000000 !important;
    }
    [data-baseweb="select"] li[aria-selected="true"] {
      background-color: #FFD700 !important;
      color: #000000 !important;
      font-weight: bold;
    }

    /* Animations */
    @keyframes dropdownFade {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
      0%   { box-shadow: 0 0 0px var(--mh-border-focus); }
      50%  { box-shadow: 0 0 20px var(--mh-border-focus); }
      100% { box-shadow: 0 0 10px var(--mh-border-focus); }
    }
    @keyframes breathingGlow {
      0%, 100% { box-shadow: 0 0 5px #FFD700; }
      50% { box-shadow: 0 0 15px #FFEA00; }
    }
    @keyframes fadeZoomIn {
      0%   { opacity: 0; transform: scale(0.9); }
      100% { opacity: 1; transform: scale(1); }
    }
    @keyframes slideInRight {
      from { opacity: 0; transform: translateX(50px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes shake {
      0% { transform: translateX(0); }
      25% { transform: translateX(-8px); }
      50% { transform: translateX(8px); }
      75% { transform: translateX(-8px); }
      100% { transform: translateX(0); }
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes buttonPulse {
      0%, 100% { transform: scale(1); box-shadow: 0 0 20px #FFD700; }
      50% { transform: scale(1.05); box-shadow: 0 0 40px #FFEA00; }
    }

    /* Login + Load forms animation */
    [data-testid="stForm"][aria-label="login_form"],
    [data-testid="stForm"][aria-label="load_form"] {
        animation: fadeZoomIn 0.8s ease;
    }
    .shake { animation: shake 0.5s; }

    /* Success & error messages */
    .stSuccess, .stError {
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
        border: 2px solid #FFD700;
        border-radius: 5px;
        padding: 10px;
        box-shadow: var(--mh-shadow);
        animation: slideInRight 0.6s ease;
    }

    /* Send button */
    [data-testid="stFormSubmitButton"] > button {
        background-color: #1a1a2e;
        color: #FFFFFF;
        border: 3px solid #FFD700;
        border-radius: 15px;
        padding: 20px 50px;
        font-size: 1.5em;
        font-weight: bold;
        box-shadow: 0 0 20px #FFD700, inset 0 0 10px rgba(255, 215, 0, 0.5);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 20px;
        text-transform: uppercase;
        animation: buttonPulse 4s infinite;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #FFD700;
        color: #1a1a2e;
        box-shadow: 0 0 30px #FFD700, 0 0 50px #FFEA00;
        transform: scale(1.05) rotate(1deg);
    }

    /* Login + Logout buttons */
    [data-testid="stButton"] > button {
        background-color: #1a1a2e;
        color: #FFFFFF;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1.1em;
        font-weight: bold;
        margin-top: 15px;
        animation: buttonPulse 5s infinite;
        transition: all 0.3s ease;
    }
    [data-testid="stButton"] > button:hover {
        background-color: #FFD700;
        color: #1a1a2e;
        box-shadow: 0 0 20px #FFD700, 0 0 40px #FFEA00;
        transform: scale(1.05);
    }

    .stForm {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- TITLE ----------------------
st.markdown('<div class="app-title">Max Hall Solutions Load Intake 🚛</div>', unsafe_allow_html=True)

# ---------------------- AUTH STATE ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False

# ---------------------- LOGIN VIEW ----------------------
if not st.session_state.logged_in:
    form_class = "shake" if st.session_state.login_failed else ""
    st.markdown(f"""<div class="{form_class}">""", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if username == "sample_customer" and password == "SamplePass2025!":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_failed = False
            st.rerun()
        else:
            st.session_state.login_failed = True
            st.error("Invalid username or password!")

# ---------------------- APP VIEW ----------------------
else:
    with st.form("load_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Origin", value="Fort Wayne, IN")
            destination = st.text_input("Destination")
            load_type = st.selectbox("Load Type", ["Steel Coils", "Scrap Metal", "General Freight"])
            weight = st.number_input("Weight (lbs)", min_value=1, value=40000)
            special_equip = st.text_input("Special Equipment", placeholder="e.g., Liftgate")
        with col2:
            truck_type = st.selectbox("Truck Type", ["Flatbed", "Dry Van", "Reefer"])
            if truck_type in ("Flatbed", "Dry Van"):
                length = st.selectbox("Length", ["48ft", "53ft"])
            else:
                length = "N/A"
            pick_date = st.date_input("Pickup Date", min_value=datetime.now(), value=datetime.now())
            pick_time = st.time_input("Pickup Time", value=time(8, 0))
            deliv_date = st.date_input("Delivery Date", min_value=pick_date + timedelta(days=1), value=pick_date + timedelta(days=1))
            deliv_time = st.time_input("Delivery Time", value=time(8, 0))
            notes = st.text_area("Special Notes", placeholder="Leave blank if none")

        if st.form_submit_button("📤 Send Load", key="unique_send_button"):
            body = f"""
            New Load from {st.session_state.username}:
            Origin: {origin}
            Destination: {destination}
            Load Type: {load_type}
            Weight: {weight} lbs
            Special Equipment: {special_equip}
            Truck Type: {truck_type} ({length})
            Pickup: {pick_date} {pick_time}
            Delivery: {deliv_date} {deliv_time}
            Notes: {notes}
            """
            msg = MIMEText(body)
            msg['Subject'] = f"New Load - {load_type}"
            msg['From'] = "whitelyonslogistics@gmail.com"
            msg['To'] = "whitelyonslogistics@gmail.com"
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("whitelyonslogistics@gmail.com", "eipoxkkifzhiwnlo")
                server.send_message(msg)
                server.quit()
                st.success("✅ Load sent to Max Hall Solutions!")
            except Exception as e:
                st.error(f"❌ Send failed: {str(e)}. Check app password.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
