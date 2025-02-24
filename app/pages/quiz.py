import streamlit as st
import json

# Load the quiz data
quiz_data = {
  "questions": [
    {
      "skill_name": "Statistical Analysis",
      "question": "Which statistical method is used to test if the means of two groups are significantly different?",
      "choices": ["Chi-Square Test", "T-Test", "Linear Regression", "K-Means Clustering"],
      "correct_answer": "T-Test"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "What is the purpose of a confidence interval?",
      "choices": ["To estimate the population mean", "To test if two groups are significantly different", "To predict future outcomes", "To describe the distribution of data"],
      "correct_answer": "To estimate the population mean"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which type of regression analysis is used to model non-linear relationships between variables?",
      "choices": ["Linear Regression", "Logistic Regression", "Decision Trees", "Polynomial Regression"],
      "correct_answer": "Polynomial Regression"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "What is the difference between a parametric and non-parametric test?",
      "choices": ["A parametric test assumes normality, while a non-parametric test does not", "A parametric test is used for categorical data, while a non-parametric test is used for continuous data", "A parametric test is used to compare means, while a non-parametric test is used to compare medians"],
      "correct_answer": "A parametric test assumes normality, while a non-parametric test does not"
    },
    {
      "skill_name": "Gen AI",
      "question": "Which technique is commonly used in Generative AI to generate realistic images?",
      "choices": ["Recurrent Neural Networks", "Transformers", "GANs", "K-Nearest Neighbors"],
      "correct_answer": "GANs"
    },
    {
      "skill_name": "Gen AI",
      "question": "What is the purpose of an Adversarial Network in Generative AI?",
      "choices": ["To generate realistic images", "To detect anomalies in data", "To optimize model performance", "To generate adversarial examples"],
      "correct_answer": "To generate adversarial examples"
    },
    {
      "skill_name": "Gen AI",
      "question": "Which type of Generative Model is used for sequence-to-sequence tasks?",
      "choices": ["VAEs", "GANs", "Transformers", "RNNs"],
      "correct_answer": "Transformers"
    },
    {
      "skill_name": "Gen AI",
      "question": "What is the difference between a Generative Model and a Discriminative Model?",
      "choices": ["A Generative Model generates new data, while a Discriminative Model predicts probabilities", "A Generative Model predicts probabilities, while a Discriminative Model generates new data"],
      "correct_answer": "A Generative Model generates new data, while a Discriminative Model predicts probabilities"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which type of regression analysis is used to model the relationship between a dependent variable and one or more independent variables?",
      "choices": ["Linear Regression", "Logistic Regression", "Decision Trees", "Polynomial Regression"],
      "correct_answer": "Linear Regression"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "What is the purpose of a hypothesis test in statistical analysis?",
      "choices": ["To estimate population parameters", "To make predictions about future outcomes", "To compare means or proportions between groups", "To describe the distribution of data"],
      "correct_answer": "To compare means or proportions between groups"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which statistical method is used to analyze time series data?",
      "choices": ["Regression Analysis", "Time Series Analysis", "Decision Trees", "K-Means Clustering"],
      "correct_answer": "Time Series Analysis"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "What is the difference between a confidence interval and a prediction interval?",
      "choices": ["A confidence interval estimates population parameters, while a prediction interval predicts future outcomes", "A confidence interval predicts future outcomes, while a prediction interval estimates population parameters"],
      "correct_answer": "A confidence interval estimates population parameters, while a prediction interval predicts future outcomes"
    },
    {
      "skill_name": "Gen AI",
      "question": "Which type of Generative Model is used for text generation?",
      "choices": ["VAEs", "GANs", "Transformers", "RNNs"],
      "correct_answer": "Transformers"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which statistical method is used to analyze categorical data?",
      "choices": ["Regression Analysis", "Time Series Analysis", "Decision Trees", "Chi-Square Test"],
      "correct_answer": "Chi-Square Test"
    },
    {
      "skill_name": "Gen AI",
      "question": "What is the purpose of a LangChain in Generative AI?",
      "choices": ["To generate realistic images", "To detect anomalies in data", "To optimize model performance", "To enable reasoning and dialogue"],
      "correct_answer": "To enable reasoning and dialogue"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which type of regression analysis is used to model non-normal data?",
      "choices": ["Linear Regression", "Logistic Regression", "Decision Trees", "Quantile Regression"],
      "correct_answer": "Quantile Regression"
    },
    {
      "skill_name": "Gen AI",
      "question": "Which type of Generative Model is used for image-to-image translation tasks?",
      "choices": ["VAEs", "GANs", "Transformers", "Pix2Pix"],
      "correct_answer": "Pix2Pix"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "What is the difference between a two-sample t-test and an ANOVA?",
      "choices": ["A two-sample t-test compares means of two groups, while an ANOVA compares means of three or more groups", "A two-sample t-test compares medians of two groups, while an ANOVA compares means of three or more groups"],
      "correct_answer": "A two-sample t-test compares means of two groups, while an ANOVA compares means of three or more groups"
    },
    {
      "skill_name": "Statistical Analysis",
      "question": "Which statistical method is used to analyze the relationship between a dependent variable and one or more independent variables?",
      "choices": ["Regression Analysis", "Time Series Analysis", "Decision Trees", "K-Means Clustering"],
      "correct_answer": "Regression Analysis"
    }
  ]
}

total_questions = len(quiz_data["questions"])

# Initialize session state variables
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = {q['question']: None for q in quiz_data["questions"]}

# Get current question
question_data = quiz_data["questions"][st.session_state.current_question]

st.title("📝 Skill-Based Quiz App")
st.write("Answer the question and navigate using the buttons below.")

st.subheader(f"Question {st.session_state.current_question + 1} of {total_questions}")
st.write(f"{question_data['question']}")
st.write(f"Skill Area: {question_data['skill_name']}")

# Display radio button for choices
selected_option = st.radio(
    "Select your answer:",
    question_data["choices"],
    index=None,
    key=question_data["question"]
)

# Store response
if selected_option:
    st.session_state.responses[question_data["question"]] = selected_option

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.current_question > 0:
        if st.button("⬅ Previous"):
            st.session_state.current_question -= 1
           

with col3:
    if st.session_state.current_question < total_questions - 1:
        if st.button("Next ➡"):
            st.session_state.current_question += 1
            

# Submit button (only visible on the last question)
if st.session_state.current_question == total_questions - 1:
    if st.button("Submit Quiz"):
        score = sum(
            1 for q in quiz_data["questions"] 
            if st.session_state.responses[q["question"]] == q["correct_answer"]
        )
        st.success(f"You scored {score} out of {total_questions}.")