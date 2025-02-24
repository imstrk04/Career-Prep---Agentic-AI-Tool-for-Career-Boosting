import streamlit as st

# Page Title
st.set_page_config(page_title="Landing Page", layout="wide")

# Custom styling for buttons
button_style = """
    <style>
        div.stButton > button {
            width: 100%;
            height: 80px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
"""

st.markdown(button_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Welcome!</h1>", unsafe_allow_html=True)

# First Row - Profile (Centered)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("👤 PROFILE"):
        st.switch_page("pages/user.py")  
col4, col5 = st.columns(2)
with col4:
    if st.button("📄 RESUME OPTIMISER"):
        st.switch_page("pages/resume_optimiser.py") 
with col5:
    if st.button("📊 SKILL GAP ANALYSIS"):
        st.switch_page("pages/skills.py")  

col6, col7 = st.columns(2)
with col6:
    if st.button("📝 QUIZ"):
        st.switch_page("pages/quiz.py")  
with col7:
    if st.button("💻 LEETCODE PROBLEMS"):
        st.switch_page("pages/leetcode.py")