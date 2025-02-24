import couchdb
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from models import UserProfile
import bcrypt


COUCHDB_URL = "http://admin:vijay123@127.0.0.1:5984/"

DB_NAME = "user-profile"

# Connect to CouchDB
try:
    couch = couchdb.Server(COUCHDB_URL)
    if DB_NAME not in couch:
        db = couch.create(DB_NAME)
    else:
        db = couch[DB_NAME]
except Exception as e:
    print(f"Database connection error: {e}")
    db = None  # Prevent operations on an uninitialized DB

class UserProfileCouch:
    @staticmethod
    def create_user_profile(user_data: dict):
        """Creates a new user profile in CouchDB."""
        try:
            if db is None:
                return {"error": "Database not initialized"}

            user_profile = UserProfile(**user_data)  # Validate with Pydantic
            user_profile._id = user_profile.contact.email  # Use email as unique ID

            if user_profile._id in db:
                return {"error": "User already exists"}

            # Convert Pydantic model to dictionary and serialize HttpUrl fields
            profile_dict = user_profile.dict()

            # 🔥 Convert HttpUrl fields to strings (only if they exist)
            if profile_dict["contact"] and profile_dict["contact"].get("linkedin"):
                profile_dict["contact"]["linkedin"] = str(profile_dict["contact"]["linkedin"])

            for project in profile_dict.get("projects", []):
                if project.get("link"):
                    project["link"] = str(project["link"])

            db[user_profile._id] = profile_dict  # Store in CouchDB
            return {"success": "User profile created successfully"}

        except Exception as e:
            return {"error": str(e)}


    @staticmethod
    def search_user_by_email(email: str):
        """Searches for a user profile by email."""
        if db is None:
            return {"error": "Database not initialized"}

        doc = db.get(email)  # Use email as `_id`
        if not doc:
            return {"error": "User not found"}
        
        return doc  # Return user profile

    @staticmethod
    def update_user_profile(email: str, updated_data: dict):
        """Updates a user profile by email."""
        if db is None:
            return {"error": "Database not initialized"}

        doc = db.get(email)
        if not doc:
            return {"error": "User not found"}

        doc.update(updated_data)  # Merge updates
        db[email] = doc  # Save changes
        return {"success": "User profile updated successfully"}

    @staticmethod
    def delete_user_profile(email: str):
        """Deletes a user profile by email."""
        if db is None:
            return {"error": "Database not initialized"}

        doc = db.get(email)
        if not doc:
            return {"error": "User not found"}

        db.delete(doc)  # Delete from CouchDB
        return {"success": "User profile deleted successfully"}

class UserAuth:  
    COUCHDB_URL = "http://admin:vijay123@127.0.0.1:5984/"
    AUTH_DB_NAME = "user-auth"  # Database for user credentials

    def __init__(self):
        """Initialize connection to CouchDB and create 'user-auth' database if not exists."""
        self.couch = couchdb.Server(self.COUCHDB_URL)
        self.auth_db = self.couch[self.AUTH_DB_NAME] if self.AUTH_DB_NAME in self.couch else self.couch.create(self.AUTH_DB_NAME)

    def hash_password(self, password: str) -> str:
        """Hashes a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def register_user(self, email: str, password: str):
        """Registers a new user with hashed password."""
        try:
            if email in self.auth_db:
                return {"error": "User already exists"}

            hashed_pw = self.hash_password(password)
            user_doc = {"_id": email, "password": hashed_pw}
            self.auth_db[email] = user_doc
            return {"success": "User registered successfully"}
        except Exception as e:
            return {"error": str(e)}

    def verify_password(self, stored_password: str, input_password: str) -> bool:
        """Verifies a password against the stored hash."""
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))

    def authenticate_user(self, email: str, password: str):
        """Authenticates a user by verifying email and password."""
        try:
            if email not in self.auth_db:
                return {"error": "User not found"}

            user_doc = self.auth_db[email]
            if self.verify_password(user_doc["password"], password):
                return {"success": "Authentication successful"}
            else:
                return {"error": "Invalid password"}
        except Exception as e:
            return {"error": str(e)}

    def delete_user(self, email: str):
        """Deletes a user from the database."""
        try:
            if email not in self.auth_db:
                return {"error": "User not found"}

            self.auth_db.delete(self.auth_db[email])
            return {"success": "User deleted successfully"}
        except Exception as e:
            return {"error": str(e)}



