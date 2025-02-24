import streamlit as st
import json
import re
import ollama
from datetime import datetime

OLLAMA_MODEL = "llama3.1:latest"
VERSIONS_DIR = "resume_versions"
MAX_ITERATIONS = 5
MIN_ATS_SCORE = 85

def clean_json_response(raw_response):
    """Clean and extract JSON from model response with logging"""
    try:
        # Log the raw response for debugging
        with st.expander("🔍 Debug: Raw Response"):
            st.code(raw_response)
        
        # Remove any leading/trailing whitespace and null bytes
        cleaned_response = raw_response.strip().replace('\x00', '')
        
        # First try to parse as pure JSON
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            with st.expander("🔍 Debug: Extracted JSON from Markdown"):
                st.code(json_str)
            return json.loads(json_str)
            
        # Try to extract anything that looks like JSON
        json_match = re.search(r'\{[\s\S]*?\}(?=\s*$)', cleaned_response)
        if json_match:
            json_str = json_match.group(0).strip()
            with st.expander("🔍 Debug: Extracted JSON from Text"):
                st.code(json_str)
            return json.loads(json_str)
            
        raise ValueError(f"Could not extract valid JSON from response")
    except Exception as e:
        st.error(f"JSON parsing error: {str(e)}")
        raise

def evaluate_ats_score(resume_json, job_description):
    """Evaluate resume's ATS compatibility score and provide feedback"""
    try:
        prompt = f"""SYSTEM: You are an ATS evaluator. Respond with ONLY a valid JSON object using this exact format:
{{
    "ats_score": number between 0 and 100,
    "keyword_matches": ["keyword1", "keyword2"],
    "missing_keywords": ["missing1", "missing2"],
    "improvement_areas": ["area1", "area2"],
    "feedback": "detailed feedback"
}}

USER: Evaluate this resume for ATS compatibility:

Job Description:
{job_description}

Resume:
{json.dumps(resume_json, indent=2)}

ASSISTANT: {{
"""
        
        # Log the prompt
        with st.expander("🔍 Debug: Evaluation Prompt"):
            st.code(prompt)
        
        # Add context to help the model complete the JSON
        messages = [
            {"role": "system", "content": "You are a resume ATS evaluator. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        raw_response = response.get("message", {}).get("content", "")
        
        # If response doesn't start with {, add it
        if not raw_response.strip().startswith("{"):
            raw_response = "{" + raw_response
        
        # If response doesn't end with }, add it
        if not raw_response.strip().endswith("}"):
            raw_response = raw_response + "}"
        
        # Try to parse the response
        evaluation = clean_json_response(raw_response)
        
        # Validate response format
        required_fields = ["ats_score", "keyword_matches", "missing_keywords", "improvement_areas", "feedback"]
        missing_fields = [field for field in required_fields if field not in evaluation]
        
        if missing_fields:
            raise ValueError(f"Response missing required fields: {', '.join(missing_fields)}")
            
        # Ensure numeric score
        try:
            evaluation["ats_score"] = float(evaluation["ats_score"])
        except (TypeError, ValueError):
            raise ValueError("Invalid ATS score format")
            
        if not 0 <= evaluation["ats_score"] <= 100:
            raise ValueError("ATS score must be between 0 and 100")
            
        # Ensure lists are actually lists
        for field in ["keyword_matches", "missing_keywords", "improvement_areas"]:
            if not isinstance(evaluation[field], list):
                evaluation[field] = [evaluation[field]] if evaluation[field] else []
                
        return evaluation
        
    except Exception as e:
        st.error(f"⚠️ ATS Evaluation Error: {str(e)}")
        return {
            "ats_score": 0,
            "keyword_matches": [],
            "missing_keywords": [],
            "improvement_areas": [f"Error in evaluation: {str(e)}"],
            "feedback": "An error occurred during evaluation. Please try again."
        }

def optimize_resume_agentic(resume_json, job_description, prev_score=0, ats_feedback=None):
    """Optimize resume using Agentic AI approach with ATS score awareness"""
    try:
        prompt = f"""SYSTEM: You are a resume optimizer. Respond with ONLY a valid JSON object matching the original resume structure.

USER: Optimize this resume to improve its ATS score of {prev_score}/100.

Previous Feedback:
{json.dumps(ats_feedback, indent=2) if ats_feedback else "Initial optimization"}

Focus on:
1. Adding missing keywords: {", ".join(ats_feedback.get("missing_keywords", [])) if ats_feedback else ""}
2. Addressing areas: {", ".join(ats_feedback.get("improvement_areas", [])) if ats_feedback else ""}
3. Quantifying achievements
4. Natural keyword integration

Job Description:
{job_description}

Current Resume:
{json.dumps(resume_json, indent=2)}

ASSISTANT: {{
"""
        
        with st.expander("🔍 Debug: Optimization Prompt"):
            st.code(prompt)
        
        # Add context to help the model complete the JSON
        messages = [
            {"role": "system", "content": "You are a resume optimizer. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        raw_response = response.get("message", {}).get("content", "")
        
        # If response doesn't start with {, add it
        if not raw_response.strip().startswith("{"):
            raw_response = "{" + raw_response
        
        # If response doesn't end with }, add it
        if not raw_response.strip().endswith("}"):
            raw_response = raw_response + "}"
        
        optimized_resume = clean_json_response(raw_response)

        required_fields = resume_json.keys()
        missing_fields = [field for field in required_fields if field not in optimized_resume]
        
        if missing_fields:
            raise ValueError(f"Optimized resume missing required fields: {', '.join(missing_fields)}")
            
        return optimized_resume
        
    except Exception as e:
        st.error(f"⚠️ Optimization Error: {str(e)}")
        return resume_json  


def generate_latex(resume_json):
    """Generate LaTeX code using the specified template format with graceful handling of missing fields"""
    
    def escape_latex(text):
        """Safely escape LaTeX special characters and handle non-string inputs"""
        if not isinstance(text, (str, int, float)):
            return str(text) if text is not None else ''
        text = str(text)
        special_chars = ['&', '%', '$', '#', '_', '{', '}', '~', '^', '\\']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text

    def get_safe_value(obj, key, default=''):
        """Safely get a value from a dictionary, handling missing keys and None values"""
        return obj.get(key, default) or default

    # Start LaTeX document
    latex_template = r"""
%------------------------
% Resume Template
% License : MIT
%------------------------

\documentclass[a4paper,10pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage[pdftex, hidelinks]{hyperref}
\usepackage{fancyhdr}

% Additional settings
\hypersetup{
    colorlinks=false,
    pdfborder={0 0 0},
}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.530in}
\addtolength{\evensidemargin}{-0.375in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.45in}
\addtolength{\textheight}{1in}

\urlstyle{rm}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
    \vspace{-10pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-6pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[2]{
    \item\small{
        \textbf{#1}{: #2 \vspace{-2pt}}
    }
}

\newcommand{\resumeSubheading}[4]{
    \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
        \textbf{#1} & #2 \\
        \textit{#3} & \textit{#4} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-3pt}}

\renewcommand{\labelitemii}{$\circ$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label=$\bullet$]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.3in]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-----------------------------
%%%%%%  CV STARTS HERE  %%%%%%

\begin{document}

%----------HEADING-----------------
\begin{center}
    \textbf{\LARGE """ + escape_latex(get_safe_value(resume_json, "name")) + r"""} \\
    \vspace{2pt}
"""

    # Handle contact information with fallbacks
    contact = resume_json.get("contact", {})
    if isinstance(contact, dict):
        email = get_safe_value(contact, "email")
        phone = get_safe_value(contact, "phone")
        linkedin = get_safe_value(contact, "linkedin")
        
        contact_parts = []
        if email:
            contact_parts.append(r"\href{mailto:" + escape_latex(email) + r"}{" + escape_latex(email) + r"}")
        if phone:
            contact_parts.append(escape_latex(phone))
        if linkedin:
            name_part = get_safe_value(resume_json, "name", "").split()[0] if get_safe_value(resume_json, "name") else "Profile"
            contact_parts.append(r"\href{" + escape_latex(linkedin) + r"}{LinkedIn: " + escape_latex(name_part) + r"}")
        
        latex_template += "    " + r" \ | \ ".join(contact_parts) + r"\\"
    else:
        # Handle contact as string or other format
        latex_template += "    " + escape_latex(str(contact)) + r"\\"

    latex_template += r"""
\end{center}

%-----------EDUCATION-----------------
\section{\textbf{Education}}
\resumeSubHeadingListStart"""

    # Education Section
    education = resume_json.get("education", [])
    if isinstance(education, list):
        for edu in education:
            if isinstance(edu, dict):
                latex_template += r"""
    \resumeSubheading
        {""" + escape_latex(get_safe_value(edu, "university")) + r"""}{""" + escape_latex(get_safe_value(edu, "location")) + r"""}
        {""" + escape_latex(get_safe_value(edu, "degree")) + r"""}{""" + escape_latex(f"{get_safe_value(edu, 'start_year')} - {get_safe_value(edu, 'end_year')}") + r"""}"""
                
                if "gpa" in edu:
                    latex_template += r"""\newline
        GPA: \textbf{""" + escape_latex(str(edu["gpa"])) + r"""}"""

    latex_template += r"""
\resumeSubHeadingListEnd

%-----------SKILLS-----------------
\section{\textbf{Skills}}
\resumeSubHeadingListStart"""

    # Skills Section
    skills = resume_json.get("skills", {})
    if isinstance(skills, dict):
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                latex_template += r"""
    \resumeSubItem{""" + escape_latex(category) + r"""}{""" + escape_latex(", ".join(skill_list)) + r"""}"""
    elif isinstance(skills, list):
        latex_template += r"""
    \resumeSubItem{Technical Skills}{""" + escape_latex(", ".join(skills)) + r"""}"""

    latex_template += r"""
\resumeSubHeadingListEnd

%-----------EXPERIENCE-----------------
\section{\textbf{Professional Experience}}
\resumeSubHeadingListStart"""

    # Experience Section
    experience = resume_json.get("experience", [])
    if isinstance(experience, list):
        for exp in experience:
            if isinstance(exp, dict):
                latex_template += r"""
    \resumeSubheading
        {""" + escape_latex(get_safe_value(exp, "company")) + r"""}{""" + escape_latex(get_safe_value(exp, "location")) + r"""}
        {""" + escape_latex(get_safe_value(exp, "position")) + r"""}{""" + escape_latex(f"{get_safe_value(exp, 'start_date')} - {get_safe_value(exp, 'end_date')}") + r"""}
    \resumeItemListStart"""
                
                responsibilities = exp.get("responsibilities", [])
                if isinstance(responsibilities, list):
                    for resp in responsibilities:
                        latex_template += r"""
        \item """ + escape_latex(resp)
                
                latex_template += r"""
    \resumeItemListEnd"""

    latex_template += r"""
\resumeSubHeadingListEnd"""

    # Projects Section (if exists)
    projects = resume_json.get("projects", [])
    if projects:
        latex_template += r"""
%-----------PROJECTS-----------------
\section{\textbf{Projects}}
\resumeSubHeadingListStart"""

        if isinstance(projects, list):
            for proj in projects:
                if isinstance(proj, dict):
                    technologies = proj.get("technologies", [])
                    tech_str = ", ".join(technologies) if isinstance(technologies, list) else str(technologies)
                    
                    latex_template += r"""
    \resumeSubItem{""" + escape_latex(get_safe_value(proj, "title")) + r"""}{""" + escape_latex(tech_str) + r"""}
    {%
    \begin{itemize}[leftmargin=*]
        \item """ + escape_latex(get_safe_value(proj, "description")) + r"""
    \end{itemize}
    }"""

        latex_template += r"""
\resumeSubHeadingListEnd"""

    # Achievements Section (if exists)
    achievements = resume_json.get("achievements", [])
    if achievements:
        latex_template += r"""
%-----------ACHIEVEMENTS-----------------
\section{\textbf{Achievements}}
\resumeSubHeadingListStart"""

        if isinstance(achievements, list):
            for achievement in achievements:
                if isinstance(achievement, dict):
                    latex_template += r"""
    \resumeSubItem{\textbf{""" + escape_latex(get_safe_value(achievement, "title")) + r"""}}{\hfill \textit{""" + escape_latex(get_safe_value(achievement, "date")) + r"""}}
    \vspace{2mm}
    \begin{itemize}[leftmargin=*]
        \item """ + escape_latex(get_safe_value(achievement, "description")) + r"""
    \end{itemize}"""

        latex_template += r"""
\resumeSubHeadingListEnd"""

    # Close document
    latex_template += r"""
%---------------------------
\end{document}"""
    
    return latex_template

def main():
    st.set_page_config(page_title="Agentic AI Resume Optimizer", page_icon="🤖", layout="wide")
    
    st.title("🤖 Agentic AI Resume Optimizer")
    st.markdown("""
    Enhance your resume with AI-powered optimization that continuously improves until reaching optimal ATS compatibility.
    1. Paste your resume in JSON format
    2. Add the target job description
    3. Watch the AI agent iterate and improve your resume
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        resume_input = st.text_area(
            "Resume JSON",
            height=300,
            help="Paste your resume in JSON format"
        )
        
    with col2:
        job_description = st.text_area(
            "💼 Job Description",
            height=300,
            help="Paste the job description you're targeting"
        )
    
    if st.button("🤖 Start Agentic Optimization", type="primary"):
        try:
            resume_json = json.loads(resume_input)
            
            # Initialize optimization tracking
            if "resume_versions" not in st.session_state:
                st.session_state.resume_versions = []
            
            # Create optimization progress container
            progress_container = st.empty()
            progress_bar = st.progress(0)
            iterations_container = st.container()
            
            current_resume = resume_json
            best_score = 0
            best_resume = None
            iteration = 0
            
            while iteration < MAX_ITERATIONS:
                iteration += 1
                progress_bar.progress(iteration / MAX_ITERATIONS)
                
                with iterations_container:
                    st.subheader(f"Iteration {iteration}")
                    
                    # Evaluate current version
                    ats_evaluation = evaluate_ats_score(current_resume, job_description)
                    current_score = ats_evaluation["ats_score"]
                    
                    # Display evaluation results
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("ATS Score", f"{current_score}/100")
                    with col2:
                        st.write("Keywords Found:", ", ".join(ats_evaluation["keyword_matches"]))
                    
                    st.write("Missing Keywords:", ", ".join(ats_evaluation["missing_keywords"]))
                    st.write("Improvement Areas:", ", ".join(ats_evaluation["improvement_areas"]))
                    
                    # Update best version if score improved
                    if current_score > best_score:
                        best_score = current_score
                        best_resume = current_resume
                        
                        # Save version
                        st.session_state.resume_versions.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "resume": current_resume,
                            "ats_score": current_score,
                            "feedback": ats_evaluation
                        })
                    
                    # Check if we've reached target score
                    if current_score >= MIN_ATS_SCORE:
                        st.success(f"Target ATS score achieved: {current_score}/100")
                        break
                    
                    # Optimize for next iteration
                    current_resume = optimize_resume_agentic(
                        current_resume,
                        job_description,
                        current_score,
                        ats_evaluation
                    )
                    
                    st.markdown("---")
            
            # Display final optimized resume
            if best_resume:
                st.subheader("Final Optimized Resume")
                tab1, tab2 = st.tabs(["JSON Output", "LaTeX Output"])
                
                with tab1:
                    st.json(best_resume)
                    
                with tab2:
                    latex_code = generate_latex(best_resume)
                    st.code(latex_code, language="latex")
                    st.download_button(
                        "⬇️ Download LaTeX",
                        latex_code,
                        file_name="optimized_resume.tex",
                        mime="text/plain"
                    )
            
            # Version History
            st.subheader("Optimization History")
            for idx, version in enumerate(reversed(st.session_state.resume_versions)):
                with st.expander(f"Version {len(st.session_state.resume_versions) - idx} - Score: {version['ats_score']}/100"):
                    st.json(version["resume"])
                    st.write("ATS Feedback:", version["feedback"])
                    
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format. Please check your input.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
