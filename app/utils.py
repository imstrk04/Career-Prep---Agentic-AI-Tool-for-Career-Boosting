# Sample User Data
from controllers import UserProfileCouch, UserAuth
new_user = {
    "name": "SADAKOPA RAMAKRISHNAN THOTHATHIRI",
    "contact": {
        "email": "sadakopa2210221@ssn.edu.in",
        "phone": "+91- 9840013841",
        "linkedin": "https://www.linkedin.com/in/sadakopa-ramakrishnan"
    },
    "education": [
        {"degree": "B.Tech IT", "university": "SSN College", "start_year": 2022, "end_year": None}
    ],
    "experience": [],
    "skills": ["Python", "Machine Learning"],
    "projects": [],
    "achievements": []
}



# # Create User
#print(UserProfileCouch.create_user_profile(new_user))

# # Search User
#print(UserProfileCouch.search_user_by_email("sadakopa2210221@ssn.edu.in"))

# # Update User
#print(UserProfileCouch.update_user_profile("sadakopa2210221@ssn.edu.in", {"name": "Sadakopa R"}))

# # Delete User
# print(UserProfileCouch.delete_user_profile("sadakopa2210221@ssn.edu.in"))

auth = UserAuth()

    # Register User
# print(auth.register_user("sadakopa2210221@ssn.edu.in", "SecurePass123"))

# # Authenticate User
# print(auth.authenticate_user("sadakopa2210221@ssn.edu.in", "SecurePass123"))

# Delete User
#print(auth.delete_user("sadakopa2210221@ssn.edu.in"))