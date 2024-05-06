# ModalDialog.py

import tkinter as tk
from tkinter import ttk

class ModalDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Select Audio Source")
        self.geometry("300x300")
        self.transient(parent)
        self.grab_set()

        # Create a variable to store the selection
        self.selected_option = tk.StringVar()

        # Create radio buttons
        self.radio_headphones = ttk.Radiobutton(self, text="Headphones", value="headphones",
                                                variable=self.selected_option)
        self.radio_default_mic = ttk.Radiobutton(self, text="Default Mic", value="default",
                                                 variable=self.selected_option)
        
        # Place the radio buttons
        self.radio_headphones.pack()
        self.radio_default_mic.pack()

        # Add an OK button
        self.ok_button = ttk.Button(self, text="OK", command=self.close_dialog)
        self.ok_button.pack()

    def close_dialog(self):

        # Get the selection
        self.master.selected_audio_source = self.selected_option.get()
        self.destroy()


