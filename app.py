import streamlit as st

    if st.button("Login"):
        hashed_password = make_hash(password)

        result = login_user(username, check_hash(password, hashed_password))

        if result:
            st.session_state.logged_in = True
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")

# =========================
# MAIN APP AFTER LOGIN
# =========================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App (KNN Improved)")

    # INPUTS
    experience = st.number_input("Experience (years)", 0, 50, 0)
    skills = st.number_input("Skills Count", 0, 50, 0)
    certifications = st.number_input("Certifications", 0, 20, 0)

    job_role = st.selectbox(
        "Job Role",
        ['Data Scientist', 'Software Engineer', 'Web Developer', 'Other']
    )

    education = st.selectbox(
        "Education",
        ['B.Tech', 'Diploma', 'M.Tech', 'Other']
    )

    location = st.selectbox(
        "Location",
        ['Bangalore', 'Hyderabad', 'Pune', 'Other']
    )

    industry = st.selectbox(
        "Industry",
        ['IT', 'Finance', 'Healthcare', 'Other']
    )

    # CREATE INPUT DATAFRAME
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
    for col in columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[columns]

    # SCALING
    input_scaled = scaler.transform(input_df)

    # PREDICTION
    if st.button("Predict Salary"):
        prediction = model.predict(input_scaled)

        st.success(f"Predicted Salary: ₹ {prediction[0]:,.2f}")

    # LOGOUT
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
