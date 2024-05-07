#sessions_view.py

import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from translation_view import TranslationView
from app_controller import AppController

class SessionsView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root)
        self.root = root
        self.controller = controller
        self.launch()
        
    def launch(self):
        # Listbox for sessions
        self.sessions_list = ttk.Treeview(self, columns=('Date', 'Duration', 'Source Language', 'Target Language'))
        self.sessions_list.heading('#0', text='Session ID')
        self.sessions_list.heading('Date', text='Date')
        self.sessions_list.heading('Duration', text='Duration')
        self.sessions_list.heading('Source Language', text='Source Language')
        self.sessions_list.heading('Target Language', text='Target Language')
        self.sessions_list.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Buttons for actions
        self.start_new_button = tk.Button(self, text="Start New Session", command=self.controller.start_new_session)
        self.start_new_button.grid(row=1, column=0, sticky='ew', padx=10)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

       
        self.pack(expand=True, fill=tk.BOTH)  # Pack the app within the root window
        self.root.mainloop()

    def load_sessions(self):
        # Placeholder: Load sessions from model
        pass

    def start_new_session(self):
        # Placeholder: Logic to start a new session
        pass    
