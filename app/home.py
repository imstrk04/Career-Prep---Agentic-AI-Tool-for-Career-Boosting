import streamlit as st # type: ignore

# Set page configuration
st.set_page_config(page_title="Career Prep", layout="wide")

# Custom CSS for button styling
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
    </style>
    """,
    unsafe_allow_html=True
)

# Create two columns for layout (text on left, image on right)
col1, col2 = st.columns([2, 3])

with col1:
    st.title("WELCOME TO CAREER PREP!")
    st.write("""
    *Your one-stop platform for interview readiness, resume building, and skill enhancement.*
    
    Get access to *mock interviews, coding challenges, and expert guidance* to boost your career prospects.
    
    Prepare with *real-world problems and industry-focused resources* to land your dream job with confidence! 🚀
    """)

    # Center-align Login and Sign Up buttons
    space1, button_col1, button_col2, space2 = st.columns([1, 2, 2, 1])

    with button_col1:
        login = st.button("Login")

    with button_col2:
        signup = st.button("Sign Up")

    # Handling button actions
    if login:
        st.switch_page("pages/login.py")
    if signup:
        st.switch_page("pages/signup.py")

# Push the image to the right by aligning it inside col2
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end;">
            <img src="https://syntaxerreur2-0.fr/wp-content/uploads/2021/10/4574122-sans-fond-980x980.png" width="700">
        </div>
        """,
        unsafe_allow_html=True
    )