# translationapp.py

import os
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kasana Translation App")
    root.geometry("1024x768")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    db = connect_db()  # Initialize your DB manager
    app = AppController(root, db)

    root.mainloop()

