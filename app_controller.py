# app_controller.py
from session_factory import SessionFactory
from speech_session import AzureSpeechTranslateSession
from new_session_view import NewSessionView

class AppController:
    def __init__(self, root):
        self.root = root
        self.factory = SessionFactory()
       
    def start_new_session(self) -> NewSessionView:
        new_session_view = NewSessionView(self.root)
        new_session_view.grab_set()  
        new_session_view.wait_window()

    def create_new_session(self) -> AzureSpeechTranslateSession:
        new_session = self.factory.create_session()
        new_session.start()
