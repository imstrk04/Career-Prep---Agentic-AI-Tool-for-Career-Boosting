import requests
import json

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql/"

def get_username_from_url(profile_url):
    return profile_url.rstrip('/').split('/')[-1]

def fetch_attempted_questions(username):
    query = """
    query recentAcSubmissions($username: String!) {
        recentAcSubmissionList(username: $username, limit: 50) {
            id
            title
            titleSlug
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {"username": username}
    }
    
    try:
        response = requests.post(LEETCODE_GRAPHQL_URL, json=payload)
        response.raise_for_status()
        
        data = response.json().get("data", {}).get("recentAcSubmissionList", [])
        
        if not data:
            print(f"No recent accepted submissions found for user: {username}")
            return []
        
        questions = [
            {"id": q["id"], "title": q["title"], "link": f"https://leetcode.com/problems/{q['titleSlug']}/"}
            for q in data
        ]
        return questions

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def save_attempted_questions(profile_url, output_file="attempted_questions.json"):
    username = get_username_from_url(profile_url)
    questions = fetch_attempted_questions(username)

    if questions:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(questions, json_file, indent=4)

        print(f"Saved {len(questions)} attempted questions to {output_file}")
    else:
        print("No questions to save.")

