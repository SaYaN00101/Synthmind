import streamlit as st
import ollama
from datetime import datetime
import mysql.connector
import uuid
import logging

# --- Logging Setup ---
logging.basicConfig(level=logging.DEBUG)

# --- Page Setup ---
st.set_page_config(page_title="SynthMind", layout='wide')

# --- MySQL Connection ---
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"])
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# --- Register User ---
def register_user(Name, Age, Gender, Country, City, UserID, password):
    try:
        conn = get_connection()
        if conn is None:
            return False
        cursor = conn.cursor()
        RegisteredAt = datetime.now()
        query = "INSERT INTO user_data(Name, Age, Gender, Country, City, UserID, password, RegisteredAt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (Name, Age, Gender, Country, City, UserID, password, RegisteredAt))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        st.error("🚫 UserID already exists. Please choose another.")
        return False
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- Authenticate User ---
def authenticate_user(UserID, password):
    try:
        conn = get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE UserID=%s AND password=%s", (UserID, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return None
    finally:
        if conn:
            conn.close()

# --- Save Messages ---
def save_message(UserID, Session_ID, Session_Title, role, content):
    try:
        conn = get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        query = "INSERT INTO chat_history (UserID, messege_role, message_content, DateTime, Session_ID, Session_Title) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (UserID, role, content, datetime.now(), Session_ID, Session_Title))
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
    finally:
        if conn:
            conn.close()

# --- Get User Sessions ---
def get_user_session(UserID):
    try:
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT Session_ID, Session_Title FROM chat_history WHERE UserID = %s GROUP BY Session_ID, Session_Title ORDER BY MAX(DateTime) DESC", (UserID,))
        sessions = cursor.fetchall()
        return sessions
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- Load Chat Messages ---
def load_session_messages(Session_ID):
    try:
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT messege_role, message_content FROM chat_history WHERE Session_ID = %s ORDER BY DateTime", (Session_ID,))
        messages = cursor.fetchall()
        return messages
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- Title Generator ---
def generate_session_title(prompt):
    return f"Chat about: {prompt[:30]}..." if prompt else "Untitled"

# --- Session State Initialization ---
for key in ["authenticated", "interaction_count", "messages", "session_id", "session_title"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "authenticated" else 0 if key == "interaction_count" else [] if key == "messages" else None

# --- New Chat Button ---
if st.sidebar.button("New Chat"):
    if st.session_state.get("authenticated") and st.session_state.get("UserID") and st.session_state.get("messages"):
        for msg in st.session_state.messages:
            save_message(
                st.session_state.UserID,
                st.session_state.session_id,
                st.session_state.session_title or "Untitled Session",
                msg["role"],
                msg["content"]
            )
    st.session_state.messages = []
    st.session_state.session_id = None
    st.session_state.session_title = None
    st.rerun()

# --- Sidebar Login/Register UI ---
st.sidebar.markdown("### User Account")
with st.sidebar.expander("Login / Register", expanded=False):
    auth_option = st.radio("Action", ["Login", "Register"])
    if not st.session_state.authenticated:
        if auth_option == "Register":
            st.sidebar.subheader("Register")
            Name = st.sidebar.text_input("Full Name")
            Age = st.sidebar.number_input("Age", min_value=0, step=1)
            Gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
            Country = st.sidebar.text_input("Country")
            City = st.sidebar.text_input("City")
            UserID = st.sidebar.text_input("User ID")
            password = st.sidebar.text_input("Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            if st.sidebar.button("Register"):
                if not all([Name, Age, Gender, Country, City, UserID, password, confirm_password]):
                    st.sidebar.warning("⚠️ Please fill all fields.")
                elif password != confirm_password:
                    st.sidebar.error("🚫 Passwords do not match.")
                else:
                    success = register_user(Name, Age, Gender, Country, City, UserID, password)
                    if success:
                        st.sidebar.success("✅ Registered successfully! Please login.")
        else:
            st.subheader("Login to SynthMind")
            UserID = st.text_input("User ID", key="login_userid")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", key="login_btn"):
                user = authenticate_user(UserID, password)
                if user:
                    st.success(f"Welcome back, {user[1]}!")
                    st.session_state.authenticated = True
                    st.session_state.UserID = UserID
                    st.session_state.messages = []
                    st.session_state.interaction_count = 0
                    st.session_state.session_id = None
                    st.session_state.session_title = None
                else:
                    st.error("🚫 Invalid credentials.")

# --- Chat History in Sidebar ---
if st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Chat History**")
    sessions = get_user_session(st.session_state.UserID)
    for session_id, session_title in sessions:
        if st.sidebar.button(session_title, key=session_id):
            st.session_state.messages = [
                {"role": role, "content": text} for role, text in load_session_messages(session_id)
            ]
            st.session_state.session_id = session_id
            st.session_state.session_title = session_title

# --- UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .title-text {
        text-align: center;
        color: #888888;
        font-size: 20px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("<div class='title-text'>What would you like to talk about or explore?</div>", unsafe_allow_html=True)

# --- Display Chat ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# --- Chat Input and Response ---
prompt = st.chat_input("Type your message here...")

if prompt:
    if not st.session_state.session_id:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.session_title = generate_session_title(prompt)

    st.session_state.interaction_count += 1

    if not st.session_state.authenticated and st.session_state.interaction_count > 3:
        st.warning("⚠️ To continue chatting with SynthMind, please login or register.")
        st.stop()

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.authenticated and "UserID" in st.session_state:
        save_message(st.session_state.UserID, st.session_state.session_id, st.session_state.session_title, "user", prompt)

    try:
        response = ollama.chat(model="gemma:2b", messages=st.session_state.messages)
        reply = response["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Error from Ollama: {e}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.session_state.authenticated and "UserID" in st.session_state:
        save_message(st.session_state.UserID, st.session_state.session_id, st.session_state.session_title, "assistant", reply)
