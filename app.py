# translationapp.py

import os
import configparser
import tkinter as tk
from app_controller import AppController
from database_manager import DatabaseManager  # Import your actual DB manager

MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

def connect_db() -> DatabaseManager:
    db_manager = DatabaseManager(MONGO_DB_URI, MONGO_DATABASE_NAME)
    if db_manager.connect():
        db = db_manager.get_database()
        return db 
    else:
        print("Database connection failed. Exiting application.")

def load_settings(file_path: str) -> dict:
    config = configparser.ConfigParser()
    config.read(file_path)
    return {
        "speech_detection_language": config.get("Settings", "speech_detection_language"),
        "audio_source": config.get("Settings", "audio_source")
    }

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kasana Ai")
    root.geometry("1024x768")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    db = connect_db()  # Initialize your DB manager

    settings = load_settings("settings.ini")  # Load settings from file
    app = AppController(root, db, settings)

    root.mainloop()

