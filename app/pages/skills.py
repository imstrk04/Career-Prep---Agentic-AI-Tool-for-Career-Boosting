import streamlit as st

# Sample skill data
skills = [
    {
        "skill_name": "Statistical Analysis",
        "concepts_to_learn": {
            "fundamentals": ["Hypothesis testing", "Confidence intervals"],
            "intermediate": ["Regression analysis", "Time series analysis"],
            "advanced": ["Bayesian methods", "Survival analysis"]
        },
        "resources": {
            "websites": [
                "https://www.statisticshowto.com",
                "https://www.khanacademy.org"
            ],
            "books": [
                "Statistical Inference - Casella & Berger",
                "Regression Analysis by Example - Simon J. Linacre"
            ],
            "courses": [
                "Statistics 101 - Coursera",
                "Data Analysis and Statistical Methods - edX"
            ]
        },
        "sample_projects": [
            {
                "title": "Analyzing the Effect of Climate Change on Sea Levels",
                "description": "Develop a statistical model to analyze the relationship between sea levels and climate change indicators"
            }
        ]
    },
    {
        "skill_name": "Gen AI",
        "concepts_to_learn": {
            "fundamentals": ["Generative models", "Adversarial training"],
            "intermediate": ["RAG methodologies", "LangChain"],
            "advanced": ["Agentic AI systems", "Transformers"]
        },
        "resources": {
            "websites": [
                "https://www.generative.ai",
                "https://langchain.dev"
            ],
            "books": [
                "Deep Learning - Ian Goodfellow, Yoshua Bengio & Aaron Courville",
                "Generative Adversarial Networks - Goodfellow et al."
            ],
            "courses": [
                "Deep Learning Specialization - Coursera",
                "Natural Language Processing with Deep Learning - edX"
            ]
        },
        "sample_projects": [
            {
                "title": "Developing an AI-Powered Chatbot for Customer Support",
                "description": "Design and implement a conversational interface using Generative AI"
            }
        ]
    }
]

# Set page configuration
st.set_page_config(page_title="Skill Learning Hub", layout="wide")

# Title
st.title("🚀 Skill Gap Analyser")

# Text box for job description
job_desc = st.text_area("🔍 Enter Job Description", placeholder="Enter job role, responsibilities, or required skills...")

# Initialize session state if not already set
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# Save job description and trigger skill summary generation
if st.button("🎯 Generate Skill Summary"):
    st.session_state.show_summary = True
    st.session_state.job_description = job_desc

# Display skills only when button is clicked
if st.session_state.show_summary:

    st.markdown("---")  # Divider

    for skill in skills:
        st.subheader(f"🛠 {skill['skill_name']}")
        
        # Concepts to Learn
        st.markdown("### 📚 Concepts to Learn")
        for level, concepts in skill["concepts_to_learn"].items():
            st.markdown(f"{level.capitalize()}")
            st.write(", ".join(concepts))

        # Resources
        st.markdown("### 🔗 Resources")
        with st.expander("🌐 Websites"):
            for link in skill["resources"]["websites"]:
                st.markdown(f"- [{link}]({link})")
        
        with st.expander("📖 Books"):
            for book in skill["resources"]["books"]:
                st.markdown(f"- {book}")

        with st.expander("🎓 Courses"):
            for course in skill["resources"]["courses"]:
                st.markdown(f"- {course}")

        # Sample Projects
        st.markdown("### 🎯 Sample Projects")
        for project in skill["sample_projects"]:
            st.markdown(f"{project['title']}")
            st.write(project["description"])

        st.markdown("---")  # Divider between skills