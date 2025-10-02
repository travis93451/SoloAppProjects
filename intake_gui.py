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
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: #FFFFFF; /* Vibrant white text */
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }

    /* ---------- Unified field styling ---------- */
    :root {
      --mh-bg: rgba(255,255,255,0.1);
      --mh-fg: #FFFFFF;
      --mh-border: #FFD700;
      --mh-border-focus: #FFEA00;
      --mh-radius: 5px;
      --mh-shadow: 0 4px 8px rgba(0,0,0,.3);
      --mh-focus: 0 0 10px var(--mh-border);
    }

    /* Text inputs */
    [data-testid="stTextInput"] input {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stTextInput"] input:focus {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }

    /* Number input */
    [data-testid="stNumberInput"] input {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stNumberInput"] input:focus {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }

    /* Selectbox */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }

    /* Date input */
    [data-testid="stDateInput"] input {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stDateInput"] input:focus {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }

    /* Time input (BaseWeb TimePicker) */
    [data-testid="stTimeInput"] div[data-baseweb="select"] {
      background-color: var(--mh-bg) !important;
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stTimeInput"] div[data-baseweb="select"]:focus-within {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }
    [data-testid="stTimeInput"] input {
      background-color: transparent !important;
      color: var(--mh-fg);
    }
    [data-testid="stTimeInput"] div[data-baseweb="select"] div[role="button"] {
      background-color: transparent !important;
    }

    /* Text area */
    [data-testid="stTextArea"] textarea {
      background-color: var(--mh-bg);
      color: var(--mh-fg);
      border: 2px solid var(--mh-border);
      border-radius: var(--mh-radius);
      box-shadow: var(--mh-shadow);
    }
    [data-testid="stTextArea"] textarea:focus {
      border-color: var(--mh-border-focus);
      box-shadow: var(--mh-focus);
    }

    /* Send Load Button */
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
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #FFD700;
        color: #1a1a2e;
        box-shadow: 0 0 30px #FFD700, 0 0 50px #FFEA00;
        transform: scale(1.05) rotate(1deg);
    }

    .stSuccess, .stError {
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFFFFF;
        border: 2px solid #FFD700;
        border-radius: 5px;
        padding: 10px;
        box-shadow: var(--mh-shadow);
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

st.title("Max Hall Solutions Load Intake 🚛")

# ---------------------- AUTH STATE ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

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
            # Optional: brief confirmation before switch
            st.success("Logged in as sample customer!")
            st.rerun()  # <-- immediately render the next screen
        else:
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
