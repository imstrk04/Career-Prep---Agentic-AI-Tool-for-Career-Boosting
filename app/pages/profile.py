import streamlit as st
import json
from controllers import UserProfileCouch

def initialize_session_state():
    if "step" not in st.session_state:
        st.session_state.step = 1
    
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "name": "",
            "contact": {
                "email": "",
                "phone": "",
                "linkedin": "",
                "github": ""
            },
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "awards": [],
            "certifications": [],
            "clubs": []
        }

def show_basic_info():
    st.header("Step 1: Basic Information")
    st.session_state.profile["name"] = st.text_input("Full Name", st.session_state.profile["name"])
    st.session_state.profile["contact"]["email"] = st.text_input("Email", st.session_state.profile["contact"]["email"])
    st.session_state.profile["contact"]["phone"] = st.text_input("Phone", st.session_state.profile["contact"]["phone"])
    st.session_state.profile["contact"]["linkedin"] = st.text_input("LinkedIn", st.session_state.profile["contact"]["linkedin"])
    st.session_state.profile["contact"]["github"] = st.text_input("GitHub", st.session_state.profile["contact"]["github"])
    
    if st.button("Next →"):
        st.session_state.step = 2
        st.rerun()

def show_fill_choice():
    st.header("Step 2: Choose Fill Method")
    choice = st.radio("Choose how to fill your profile:", ["Upload Resume", "Manual"])
    
    if choice == "Upload Resume":
        uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])
        
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            if st.button("Continue with Manual Edit"):
                autofill_data()
                st.session_state.step = 3
                st.rerun()
    
    if st.button("Next →"):
        st.session_state.step = 3
        st.rerun()
    
    if st.button("← Back"):
        st.session_state.step = 1
        st.rerun()

def autofill_data():
    # Predefined data for autofill
    autofill_data = {
  "name": "SADAKOPA RAMAKRISHNAN THOTHATHIRI",
  "contact": {
    "email": "sadakopa2210221@ssn.edu.in",
    "phone": "+91-9840013841",
    "linkedin": "https://www.linkedin.com/in/sadakopa-ramakrishnan"
  },
  "education": [
    {
      "degree": "Bachelor of Technology - Information Technology",
      "university": "Sri Sivasubramaniya Nadar College of Engineering, Kalavakkam Chennai, India",
      "start_year": 2022,
      "end_year": None
    },
    {
      "degree": "Diploma in Programming and Data Science",
      "university": "Indian Institute Of Technology, Madras Chennai, India",
      "start_year": 2023,
      "end_year": None
    }
  ],
  "experience": [
    {
      "position": "Machine Learning Engineer Intern",
      "company": "DigiTwin Technology Remote",
      "start_date": "November 2024",
      "end_date": None,
      "responsibilities": [
        "Participated in the development and fine-tuning of Large Language Models (LLMs) and Small Language Models (SLMs)",
        "Gained hands-on experience with LangChain and RAG methodologies, integrating them to build effective AI-driven solutions",
        "Contributed to the design and development of Agentic AI systems"
      ]
    }
  ],
  "skills": [
    "Python",
    "Java",
    "JavaScript",
    "Firebase",
    "MySQL",
    "Oracle SQL* Plus",
    "SQLite",
    "Git",
    "GitHub",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "NumPy",
    "Pandas",
    "Matplotlib",
    "Seaborn",
    "XGBoost"
  ],
  "projects": [
    {
      "title": "System Threat Forecaster",
      "description": "Developed a malware infection prediction model using threat telemetry data from antivirus software having over 76 columns.",
      "technologies": ["Python", "scikit-learn", "numpy", "pandas"],
      "link": None
    },
    {
      "title": "Two-stage Flight Delay Predictor",
      "description": "Developed a dual-stage machine learning model to forecast flight delays at 15 major U.S. airports using 2016-2017 flight and weather data.",
      "technologies": ["Python", "scikit", "numpy", "pandas"],
      "link": "https://github.com/"
    },
    {
      "title": "RAG System - Chat & Learn",
      "description": "Designed a Retrieval-Augmented Generation (RAG) system to extract insights from 50+ NCERT textbooks using NVIDIA NIM and vector databases.",
      "technologies": ["Python", "NVIDIA NIM", "Vector Database"],
      "link": "https://github.com/"
    },
    {
      "title": "AI-Powered Test Case Generator",
      "description": "Built a Streamlit app generating manual test cases for image-based functionalities using Google’s Gemini API.",
      "technologies": ["Python", "Streamlit", "Google Gemini API"],
      "link": "https://github.com/"
    }
  ],
  "achievements": [
    {
      "title": "HackIT Finalist",
      "year": "Nov 2023"
    },
    {
      "title": "SIH’23 - Internal Hackathon Winner",
      "year": "Sep 2023"
    },
    {
      "title": "Adobe GenSolve Hackathon 2024",
      "year": "July 2024"
    }
  ]
}
    st.session_state.profile.update(autofill_data)

def show_education():
    st.header("Step 3: Education")
    
    if len(st.session_state.profile["education"]) == 0:
        st.session_state.profile["education"].append({
            "degree": "",
            "university": "",
            "location": "",
            "start_year": "",
            "end_year": "",
            "gpa": ""
        })
    
    for i, edu in enumerate(st.session_state.profile["education"]):
        st.subheader(f"Education #{i+1}")
        edu["degree"] = st.text_input(f"Degree", edu["degree"], key=f"degree_{i}")
        edu["university"] = st.text_input(f"University", edu["university"], key=f"university_{i}")
        edu["location"] = st.text_input(f"Location", edu.get("location", ""), key=f"location_{i}")
        col1, col2 = st.columns(2)
        with col1:
            edu["start_year"] = st.text_input(f"Start Year", edu.get("start_year", ""), key=f"start_year_{i}")
        with col2:
            edu["end_year"] = st.text_input(f"End Year", edu.get("end_year", ""), key=f"end_year_{i}")
        edu["gpa"] = st.text_input(f"GPA", edu.get("gpa", ""), key=f"gpa_{i}")
    
    if st.button("Add Another Education"):
        st.session_state.profile["education"].append({
            "degree": "",
            "university": "",
            "location": "",
            "start_year": "",
            "end_year": "",
            "gpa": ""
        })
        st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.step = 4
            st.rerun()

def show_experience():
    st.header("Step 4: Work Experience")
    
    if len(st.session_state.profile["experience"]) == 0:
        st.session_state.profile["experience"].append({
            "position": "",
            "company": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "responsibilities": []
        })
    
    for i, exp in enumerate(st.session_state.profile["experience"]):
        st.subheader(f"Experience #{i+1}")
        exp["position"] = st.text_input(f"Position", exp["position"], key=f"position_{i}")
        exp["company"] = st.text_input(f"Company", exp["company"], key=f"company_{i}")
        exp["location"] = st.text_input(f"Location", exp.get("location", ""), key=f"location_{i}")
        col1, col2 = st.columns(2)
        with col1:
            exp["start_date"] = st.text_input(f"Start Date", exp.get("start_date", ""), key=f"start_date_{i}")
        with col2:
            exp["end_date"] = st.text_input(f"End Date", exp.get("end_date", ""), key=f"end_date_{i}")
        
        responsibilities = "\n".join(exp.get("responsibilities", []))
        responsibilities = st.text_area(
            "Responsibilities (one per line)",
            responsibilities,
            key=f"responsibilities_{i}"
        )
        exp["responsibilities"] = [r.strip() for r in responsibilities.split("\n") if r.strip()]
    
    if st.button("Add Another Experience"):
        st.session_state.profile["experience"].append({
            "position": "",
            "company": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "responsibilities": []
        })
        st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.step = 5
            st.rerun()

def show_skills():
    st.header("Step 5: Skills")
    
    skills_text = st.text_area(
        "Enter your skills (one per line):",
        "\n".join(st.session_state.profile["skills"])
    )
    st.session_state.profile["skills"] = [s.strip() for s in skills_text.split("\n") if s.strip()]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.step = 6
            st.rerun()

st.title("Resume Builder")

# Initialize session state
initialize_session_state()

# Show progress bar
st.progress(st.session_state.step / 6)

# Display current step
if st.session_state.step == 1:
    show_basic_info()
elif st.session_state.step == 2:
    show_fill_choice()
elif st.session_state.step == 3:
    show_education()
elif st.session_state.step == 4:
    show_experience()
elif st.session_state.step == 5:
    show_skills()
elif st.session_state.step == 6:
    res = UserProfileCouch.create_user_profile(st.session_state["profile"])
    if 'success' in res:
        st.success("Profile Saved Successfully!")
    else:
        st.error(res)
    userHome = st.button(" Go back to User Home")
    if userHome:
        st.switch_page("pages/UserHome.py")
    