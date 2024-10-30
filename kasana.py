# translationapp.py

import os
import tkinter as tk
from app_controller import AppController
from user_settings import UserSettings

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kasana")
    root.geometry("1024x768")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    user_settings = UserSettings()
    app = AppController(root, user_settings)
    root.mainloop()

