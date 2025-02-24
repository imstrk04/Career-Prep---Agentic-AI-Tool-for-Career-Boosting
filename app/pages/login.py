import streamlit as st # type: ignore
from controllers import UserAuth
# Set page configuration
st.set_page_config(page_title="Login", layout="wide")

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
    st.switch_page("home.py")
st.markdown('</div>', unsafe_allow_html=True)

# Center-align the login form
st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

# Login form
with st.form(key="login_form", clear_on_submit=True):
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")


    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<a href='#' style='text-decoration: none; color: #4da6ff;'>Forgot Password?</a>", unsafe_allow_html=True)
    
    with col2:
        login_btn = st.form_submit_button("Login")

# Handling login action
if login_btn:
    if email and password:
        auth = UserAuth()
        res = auth.authenticate_user(email, password)
        if 'success' in res:
            st.success("Login Successful!")
            st.switch_page("pages/profile.py")
    else:
        st.error("Please enter email and password.")

# Sign-up option
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Don't have an account? <a href='signup' style='color: #4da6ff;'>Sign Up</a></p>", unsafe_allow_html=True)