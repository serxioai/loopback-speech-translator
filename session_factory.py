import uuid
from speech_session import AzureSpeechTranslateSession

class SessionFactory:
    def __init__(self):
        self.current_session = None
        self.sessions = {}
    
    def create_session(self, config) -> AzureSpeechTranslateSession:
        if self.current_session is not None:
            self.current_session.stop()
            self.current_session.save_translations()
        session_id = str(uuid.uuid4())
        new_session = AzureSpeechTranslateSession(session_id, config)
        self.sessions[session_id] = new_session
        self.current_session = new_session
        self.current_session.configure()  # Ensure the session is configured
        self.current_session.start()
        return new_session
    