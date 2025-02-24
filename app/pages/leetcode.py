import streamlit as st
import json
import random

# Load attempted questions (Revisit)
def load_attempted_questions(filename="attempted_questions.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Load all available LeetCode questions (Try These)
def load_leetcode_questions(filename="leetcode_questions.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Streamlit UI
st.title("LeetCode Problem Tracker")

revisit_problems = load_attempted_questions()
all_questions = load_leetcode_questions()

# Select 20 random problems for "TRY THESE!" section
try_problems = random.sample(all_questions, min(20, len(all_questions)))

# Create two columns for displaying problems side by side
col1, col2 = st.columns(2)

with col1:
    st.header("🛠 REVISIT THEM!")
    for problem in revisit_problems:
        st.markdown(f"- [{problem['title']}]({problem['link']})")

with col2:
    st.header("🚀 TRY THESE!")
    for problem in try_problems:
        st.markdown(f"- [{problem['title']}]({problem['link']})")