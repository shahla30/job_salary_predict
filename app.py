import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import joblib

# =========================
# DATABASE CONNECTION
# =========================
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# =========================
# CREATE TABLE
# =========================
c.execute('''
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
''')

conn.commit()

# =========================
# HASH PASSWORD
# =========================
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# =========================
# ADD USER
# =========================
def add_user(username, password):
    c.execute(
        'INSERT INTO users(username, password) VALUES (?, ?)',
        (username, password)
    )
    conn.commit()

# =========================
# LOGIN USER
# =========================
def login_user(username, password):
    c.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    )
    data = c.fetchall()
    return data

# =========================
# LOAD MODEL FILES
# =========================
model = joblib.load('knn_model.pkl')
scaler = joblib.load('scaler.pkl')
columns = joblib.load('columns.pkl')

# =========================
# SESSION STATE
# =========================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# =========================
# SIDEBAR MENU
# =========================
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

# =========================
# SIGNUP PAGE
# =========================
if choice == "Signup":

    st.title("Create New Account")

    new_user = st.text_input("Username")

    new_password = st.text_input(
        "Password",
        type='password'
    )

    if st.button("Signup"):

        hashed_password = make_hash(new_password)

        add_user(new_user, hashed_password)

        st.success("Account created successfully!")

        st.info("Go to Login page to login")

# =========================
# LOGIN PAGE
# =========================
elif choice == "Login":

    st.title("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type='password'
    )

    if st.button("Login"):

        hashed_password = make_hash(password)

        result = login_user(
            username,
            hashed_password
        )

        if result:

            st.session_state.logged_in = True

            st.success(f"Welcome {username}!")

        else:

            st.error("Invalid username or password")

# =========================
# MAIN APP
# =========================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App (KNN Improved)")

    # INPUTS
    experience = st.number_input(
        "Experience (years)",
        0,
        50,
        0
    )

    skills = st.number_input(
        "Skills Count",
        0,
        50,
        0
    )

    certifications = st.number_input(
        "Certifications",
        0,
        20,
        0
    )

    job_role = st.selectbox(
        "Job Role",
        [
            'Data Scientist',
            'Software Engineer',
            'Web Developer',
            'Other'
        ]
    )

    education = st.selectbox(
        "Education",
        [
            'B.Tech',
            'Diploma',
            'M.Tech',
            'Other'
        ]
    )

    location = st.selectbox(
        "Location",
        [
            'Bangalore',
            'Hyderabad',
            'Pune',
            'Other'
        ]
    )

    industry = st.selectbox(
        "Industry",
        [
            'IT',
            'Finance',
            'Healthcare',
            'Other'
        ]
    )

    # CREATE INPUT DATA
    input_dict = {
        'Experience': [experience],
        'Skills': [skills],
        'Certifications': [certifications],
        'Job_Role': [job_role],
        'Education': [education],
        'Location': [location],
        'Industry': [industry]
    }

    input_df = pd.DataFrame(input_dict)

    # ONE HOT ENCODING
    input_df = pd.get_dummies(input_df)

    # MATCH TRAINING COLUMNS
input_df = input_df.reindex(
    columns=columns,
    fill_value=0
)

    # SCALE DATA
    input_scaled = scaler.transform(input_df)

    # PREDICT
    if st.button("Predict Salary"):

        prediction = model.predict(input_scaled)

        st.success(
            f"Predicted Salary: ₹ {prediction[0]:,.2f}"
        )

    # LOGOUT
    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()
