import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Max Hall Solutions Load Intake", layout="wide")

# ---------------------- THEME / CSS ----------------------
st.markdown(
    """
    <style>
    /* ---------- App background ---------- */
    .stApp {
        background:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
            url("https://raw.githubusercontent.com/travis93451/SoloAppProjects/main/assets/abstract_bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }

    /* ---------- Design tokens ---------- */
    :root{
      --mh-bg: #FFFFFF;        /* input background */
      --mh-fg: #000000;        /* input text */
      --mh-border: #FFD700;    /* default border */
      --mh-border-focus:#FFEA00; /* focus border */
      --mh-radius: 6px;
      --mh-shadow: 0 4px 8px rgba(0,0,0,.28);
      --mh-placeholder:#6B7280; /* gray-500 */
      --mh-label:#F9FAFB;        /* label text (near-white) */
    }

    /* ---------- Form labels (desktop & mobile) ---------- */
    .stApp label{
      color: var(--mh-label) !important;
      font-weight: 600;
      text-shadow: 0 1px 4px rgba(0,0,0,.55);
      letter-spacing:.1px;
    }
    @media (max-width: 640px){
      .stApp label{
        color:#FFFFFF !important;
        text-shadow: 0 0 8px rgba(0,0,0,.85);
      }
    }

    /* Placeholder color */
    input::placeholder, textarea::placeholder{ color: var(--mh-placeholder); opacity:1; }

    /* ---------- Title ---------- */
    .app-title{
        font-size: 2.5em;
        text-align:center;
        margin-bottom: 20px;
        font-weight: 800;
        color:#FFD700;
        text-shadow: 0 0 10px #FFD700, 0 0 22px #FFEA00, 0 0 34px #FFEA00;
        animation: titleGlow 2s infinite alternate;
    }
    @keyframes titleGlow{
        0%{ text-shadow: 0 0 10px #FFD700, 0 0 22px #FFEA00; }
        50%{ text-shadow: 0 0 20px #FFD700, 0 0 42px #FFEA00, 0 0 60px #FFEA00; }
        100%{ text-shadow: 0 0 10px #FFD700, 0 0 22px #FFEA00; }
    }

    /* ---------- UNIFIED FIELD STYLE ----------
       Make ALL widgets (text, number, date, time, textarea, select)
       look identical: white bg, black text, gold border.             */
    /* Text, Number, Date, Time, Textarea inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input,
    [data-testid="stTextArea"] textarea{
      background-color: var(--mh-bg) !important;
      color: var(--mh-fg) !important;
      border: 2px solid var(--mh-border) !important;
      border-radius: var(--mh-radius) !important;
      box-shadow: var(--mh-shadow) !important;
      animation: breathingGlow 3s infinite ease-in-out;
    }

    /* BaseWeb select/time picker container (ensures same look) */
    [data-baseweb="select"]{
      background-color: var(--mh-bg) !important;
      color: var(--mh-fg) !important;
      border: 2px solid var(--mh-border) !important;
      border-radius: var(--mh-radius) !important;
      box-shadow: var(--mh-shadow) !important;
    }
    /* Inner pieces of BaseWeb select */
    [data-baseweb="select"] *{
      color: var(--mh-fg) !important;
      background-color: transparent !important;
    }
    /* The visible value area */
    [data-baseweb="select"] > div{
      background-color: var(--mh-bg) !important;
    }

    /* Focus states (all fields) */
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus,
    [data-testid="stTimeInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-baseweb="select"]:focus-within{
      border-color: var(--mh-border-focus) !important;
      box-shadow: 0 0 15px var(--mh-border-focus) !important;
      animation: pulseGlow .6s ease;
    }

    /* Number stepper buttons */
    [data-testid="stNumberInput"] button{
      background-color:#111827 !important; /* near-black */
      color:#FFD700 !important;
      border:1px solid var(--mh-border) !important;
      border-radius:4px !important;
      transition: all .25s ease;
    }
    [data-testid="stNumberInput"] button:hover{
      background-color:#FFD700 !important;
      color:#111827 !important;
      box-shadow:0 0 10px #FFD700 !important;
      transform: scale(1.08);
    }

    /* Dropdown menu items (list) */
    [data-baseweb="select"] li{
      background-color:#FFFFFF !important;
      color:#000000 !important;
      opacity:0; transform: translateY(-8px);
      animation: dropdownFade .22s ease forwards;
    }
    [data-baseweb="select"] li:hover{
      background-color:#FFD700 !important; color:#000000 !important;
    }
    [data-baseweb="select"] li[aria-selected="true"]{
      background-color:#FFD700 !important; color:#000000 !important;
      font-weight:700;
    }

    /* Animations */
    @keyframes dropdownFade{ from{opacity:0; transform:translateY(-8px);} to{opacity:1; transform:translateY(0);} }
    @keyframes pulseGlow{ 0%{box-shadow:0 0 0 var(--mh-border-focus);} 50%{box-shadow:0 0 18px var(--mh-border-focus);} 100%{box-shadow:0 0 8px var(--mh-border-focus);} }
    @keyframes breathingGlow{ 0%,100%{ box-shadow:0 0 5px #FFD700; } 50%{ box-shadow:0 0 14px #FFEA00; } }

    /* Forms container */
    .stForm{
      background-color: rgba(0,0,0,0.45);
      padding: 20px; border-radius: 10px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.55);
      backdrop-filter: blur(2px);
    }

    /* Success & error messages */
    .stSuccess,.stError{
      background-color: rgba(0,0,0,0.55);
      color:#FFF; border:2px solid #FFD700; border-radius:6px;
      padding:10px; box-shadow: var(--mh-shadow);
    }

    /* Buttons */
    @keyframes buttonPulse{ 0%,100%{transform:scale(1); box-shadow:0 0 20px #FFD700;} 50%{transform:scale(1.05); box-shadow:0 0 40px #FFEA00;} }

    [data-testid="stFormSubmitButton"] > button{
      background-color:#111827; color:#FFFFFF;
      border:3px solid #FFD700; border-radius:14px;
      padding:18px 44px; font-size:1.35em; font-weight:800;
      text-transform:uppercase; width:100%;
      box-shadow: 0 0 20px #FFD700, inset 0 0 10px rgba(255,215,0,.45);
      transition: all .25s ease; margin-top:20px;
      animation: buttonPulse 4s infinite;
    }
    [data-testid="stFormSubmitButton"] > button:hover{
      background:#FFD700; color:#111827;
      box-shadow:0 0 34px #FFD700, 0 0 54px #FFEA00;
      transform: scale(1.05) rotate(1deg);
    }

    [data-testid="stButton"] > button{
      background-color:#111827; color:#FFFFFF;
      border:2px solid #FFD700; border-radius:10px;
      padding:12px 30px; font-size:1.05em; font-weight:700;
      margin-top:15px; transition: all .25s ease;
      animation: buttonPulse 5s infinite;
    }
    [data-testid="stButton"] > button:hover{
      background:#FFD700; color:#111827;
      box-shadow:0 0 22px #FFD700, 0 0 40px #FFEA00; transform: scale(1.05);
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
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

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
