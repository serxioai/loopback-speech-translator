# app_controller.py

import tkinter as tk
from session_factory import SessionFactory
from new_session_view import NewSessionView
from translation_view import TranslationView
from sessions_view import SessionsView

class AppController:
    def __init__(self, root):
        self.root = root
        self.factory = SessionFactory()
        self.current_view = None
        self.launch_sessions_view()
       
    def launch_sessions_view(self):
        if self.current_view:
            self.current_view.pack_forget()  # Hide the current view
        self.current_view = SessionsView(self.root, self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def launch_new_session_view(self) -> NewSessionView:
        session_view = NewSessionView(self.root, self.on_init_new_session)

    def launch_translation_view(self, session):
        if self.current_view:
            self.current_view.pack_forget()  # Hide the current view
        self.current_view = TranslationView(self.root, session)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def on_init_new_session(self, data):
        session = self.factory.create_session(data)
        self.launch_translation_view(session)

    def end_session(self):
        pass

    def save_session(self):
        pass