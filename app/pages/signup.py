import streamlit as st
from controllers import UserAuth
# Set page configuration
st.set_page_config(page_title="Sign Up", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4da6ff; /* Light Blue */
        color: white;
        border-radius: 8px;
        width: 120px;
        height: 45px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3399ff; /* Slightly Darker Blue */
    }
    .home-btn {
        position: absolute;
        top: 10px;
        right: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home button (top-right corner)
st.markdown('<div class="home-btn">', unsafe_allow_html=True)
if st.button("🏠 Home"):
    st.switch_page("home")
st.markdown('</div>', unsafe_allow_html=True)

# Center-align the sign-up form
st.markdown("<h1 style='text-align: center;'>Sign Up</h1>", unsafe_allow_html=True)

# Sign-up form
with st.form(key="signup_form", clear_on_submit=True):
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    col1, col2 = st.columns([1, 1])

    with col2:
        sign_up_btn = st.form_submit_button("Signup")

# Handling sign-up action
if sign_up_btn:
    if not email or not password or not confirm_password:
        st.error("All fields are required!")
    elif password != confirm_password:
        st.error("Passwords do not match!")
    else:
        auth = UserAuth()
        auth.register_user(email, password)
        st.success("Account created successfully!")
        

        

# Login option
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Go to login? <a href='pages/login.py' style='color: #4da6ff;'>Login</a></p>", unsafe_allow_html=True)