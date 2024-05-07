# translationapp.py

import tkinter as tk
from app_controller import AppController
from sessions_view import SessionsView

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800") 
    root.title("Azure Speech Translator") 
    controller = AppController(root)
    main_view = SessionsView(root, controller)
    main_view.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

    