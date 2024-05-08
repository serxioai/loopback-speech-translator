# app_controller.py

from session_factory import SessionFactory
from new_session_view import NewSessionView

class AppController:
    def __init__(self, root):
        self.root = root
        self.factory = SessionFactory()
       
    def launch_new_session_view(self) -> NewSessionView:
        session_view = NewSessionView(self.root, self.on_new_session_created)
        session_view.wait_window()

    def on_new_session_created(self, data):
        print(f"SESSION DATA {data}")
        session = self.factory.create_session(data)
        

    def end_session(self):
        pass

    def save_session(self):
        pass