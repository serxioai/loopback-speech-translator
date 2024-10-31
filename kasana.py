# translationapp.py

import logging
import tkinter as tk
from logging.handlers import RotatingFileHandler
from app_controller import AppController
from user_settings import UserSettings

# Set up logging configuration at the start of the application
logging.basicConfig(
    filename='kasana.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# For production, you might want to add log rotation to prevent huge log files
root_logger = logging.getLogger()
handler = RotatingFileHandler(
    'kasana.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5
)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(handler)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kasana")
    root.geometry("1024x768")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    user_settings = UserSettings()
    app = AppController(root, user_settings)
    root.mainloop()

