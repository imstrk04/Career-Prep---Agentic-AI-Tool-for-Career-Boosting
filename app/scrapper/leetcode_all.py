import requests
import json

# LeetCode API URL
URL = "https://leetcode.com/api/problems/all/"

# Fetch problems data
response = requests.get(URL)
data = response.json()

# Extract question details
questions = []
for question in data['stat_status_pairs']:
    question_id = question['stat']['frontend_question_id']  # Question number
    title = question['stat']['question__title']
    slug = question['stat']['question__title_slug']
    difficulty = ["Easy", "Medium", "Hard"][question['difficulty']['level'] - 1]  # Convert level to text
    link = f"https://leetcode.com/problems/{slug}/"

    questions.append({
        "id": question_id,
        "title": title,
        "difficulty": difficulty,
        "link": link
    })

# Save as JSON
with open("leetcode_questions.json", "w") as f:
    json.dump(questions, f, indent=4)

print("Data saved to leetcode_questions.json")
