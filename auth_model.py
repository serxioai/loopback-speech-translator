import os
import requests
from pymongo import MongoClient

class AuthModel:
    def __init__(self):
        self.AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
        self.CLIENT_ID = os.environ.get("CLIENT_ID")
        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        self.API_IDENTIFIER = os.environ.get("API_IDENTIFIER")
        self.REDIRECT_URI = "http://localhost:8000/callback"
        self.mongo_client = MongoClient(os.getenv("MONGO_DB_URI"))
        self.db = self.mongo_client[os.environ.get("MONGO_DATABASE_NAME")]
        self.users_collection = self.db["users"]

    def get_auth_url(self):
        return f"https://{self.AUTH0_DOMAIN}/authorize?audience={self.API_IDENTIFIER}&response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}"

    def process_auth_response(self, code):
        url = f"https://{self.AUTH0_DOMAIN}/oauth/token"
        headers = {'content-type': 'application/json'}
        data = {
            "grant_type": "authorization_code",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "code": code,
            "redirect_uri": self.REDIRECT_URI
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def register_user(self, email, username, password):
        try:
            user = {
                "email": email,
                "username": username,
                "password": password
            }
            print("Attempting to insert user:", user)
            self.users_collection.insert_one(user)
            print("User inserted successfully.")
        except Exception as e:
            print("Error occurred while inserting user:", str(e))

    def authenticate_user(self, username, password):
        user = self.users_collection.find_one({"username": username})
        if user and user["password"] == password:
            return user  # Return the user document
        return None  # Return None if authentication fails

