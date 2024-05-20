# translationapp.py

import tkinter as tk
from app_controller import AppController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Serxio AI")
    root.geometry("1024x768")  # Set a default size if needed
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = AppController(root)
    root.mainloop()