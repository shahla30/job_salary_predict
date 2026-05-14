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
# =========================
# MAIN APP
# =========================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    # INPUTS
    experience = st.number_input("Experience Years", 0, 50, 1)

    skills = st.number_input("Skills Count", 0, 50, 1)

    certifications = st.number_input("Certifications", 0, 20, 0)

    job_title = st.selectbox(
        "Job Title",
        [
            "Backend Developer",
            "Business Analyst",
            "Cloud Engineer",
            "Cybersecurity Analyst",
            "Data Analyst",
            "Data Scientist",
            "DevOps Engineer",
            "Frontend Developer",
            "Machine Learning Engineer",
            "Product Manager",
            "Software Engineer"
        ]
    )

    education = st.selectbox(
        "Education Level",
        [
            "Diploma",
            "High School",
            "Master",
            "PhD"
        ]
    )

    location = st.selectbox(
        "Location",
        [
            "Canada",
            "Germany",
            "India",
            "Netherlands",
            "Remote",
            "Singapore",
            "Sweden",
            "UK",
            "USA"
        ]
    )

    industry = st.selectbox(
        "Industry",
        [
            "Education",
            "Finance",
            "Government",
            "Healthcare",
            "Manufacturing",
            "Media",
            "Retail",
            "Technology",
            "Telecom"
        ]
    )

    company_size = st.selectbox(
        "Company Size",
        [
            "Large",
            "Medium",
            "Small",
            "Startup"
        ]
    )

    remote_work = st.selectbox(
        "Remote Work",
        [
            "Yes",
            "No"
        ]
    )

    seniority = st.selectbox(
        "Seniority",
        [
            "Junior",
            "Mid",
            "Senior"
        ]
    )

    if st.button("Predict Salary"):

        input_data = dict.fromkeys(columns, 0)

        # NUMERIC FEATURES
        input_data['experience_years'] = experience
        input_data['skills_count'] = skills
        input_data['certifications'] = certifications

        input_data['exp_squared'] = experience ** 2
        input_data['skill_per_exp'] = skills / (experience + 1)
        input_data['cert_per_skill'] = certifications / (skills + 1)

        # ONE HOT ENCODED FEATURES
        input_data[f'job_title_{job_title}'] = 1
        input_data[f'education_level_{education}'] = 1
        input_data[f'location_{location}'] = 1
        input_data[f'industry_{industry}'] = 1
        input_data[f'company_size_{company_size}'] = 1
        input_data[f'remote_work_{remote_work}'] = 1
        input_data[f'seniority_{seniority}'] = 1

        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)

        st.success(
            f"💰 Predicted Salary: ₹ {prediction[0]:,.2f}"
        )

    # LOGOUT
    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()
