# translationapp.py

import tkinter as tk
from app_controller import AppController

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800") 
    root.title("Azure Speech Translator") 
    controller = AppController(root)
    root.mainloop()