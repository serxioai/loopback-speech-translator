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
        self.current_session = None
        self.new_session_view = None
        self.launch_sessions_view()
       
    def launch_sessions_view(self):
        if self.current_view:
            self.current_view.pack_forget()  # Hide the current view
        self.current_view = SessionsView(self.root, self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def launch_new_session_view(self) -> NewSessionView:
        self.new_session_view = NewSessionView(self.root, 
                                               self.on_init_new_session_callback)

    def launch_translation_view_callback(self) -> TranslationView:
        if self.current_view:
            self.current_view.pack_forget()  # Hide the current view
        self.current_view = TranslationView(self.current_session, 
                                            self.root, 
                                            self.on_start_speech_session_callback,
                                            self.on_stop_speech_session_callback,
                                            self.on_change_recognizing_event_rate_callback,
                                            )

    def on_init_new_session_callback(self, data):
        self.current_session = self.factory.create_session(data)
        self.launch_translation_view_callback()

    def on_start_speech_session_callback(self):
        self.current_session.start()

    def on_stop_speech_session_callback(self):
        self.current_session.stop()

    def on_change_recognizing_event_rate_callback(self, rate):
        self.current_session.set_recognizing_event_rate(rate)

    def end_session(self):
        pass

    def save_session(self):
        pass