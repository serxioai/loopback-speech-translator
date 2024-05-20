#sessions_view.py

import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from translation_view import TranslationView
from config_session_view import ConfigSessionView

class SessionsView(tk.Frame):
    def __init__(self, root, config_session_callback):
        super().__init__(root)
        self.root = root
        self.config_session_callback = config_session_callback
        self.build_ui()
        
    def build_ui(self):
        # Listbox for sessions
        self.sessions_list = ttk.Treeview(self, columns=('Date', 'Duration', 'Source Language', 'Target Language'))
        self.sessions_list.heading('#0', text='Session ID')
        self.sessions_list.heading('Date', text='Date')
        self.sessions_list.heading('Duration', text='Duration')
        self.sessions_list.heading('Source Language', text='Source Language')
        self.sessions_list.heading('Target Language', text='Target Language')
        self.sessions_list.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Buttons for actions
        self.start_new_button = tk.Button(self, text="Start New Session", command=self.on_new_session_pressed)
        self.start_new_button.grid(row=1, column=0, sticky='ew', padx=10)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
       
        self.pack(expand=True, fill=tk.BOTH)  # Pack the app within the root window
        self.load_sessions()

    def on_new_session_pressed(self):
        self.config_session_callback()

    def load_sessions(self):
        # Simulated data
        sessions = [
            {"id": "1", "date": "2024-05-10", "duration": "30 mins", "source_lang": "EN", "target_lang": "ES"},
            {"id": "2", "date": "2024-05-11", "duration": "45 mins", "source_lang": "EN", "target_lang": "FR"}
        ]
        for session in sessions:
            self.sessions_list.insert("", 'end', id=session["id"], text=session["id"],
                                    values=(session["date"], session["duration"], session["source_lang"], session["target_lang"]))
