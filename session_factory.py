import uuid
from speech_session import AzureSpeechTranslateSession

class SessionFactory:
    def __init__(self, db_manager):
        self.current_session = None
        self.sessions = {}
        self.db_manager = db_manager
        self.user_id = None
    
    def init_session(self, config) -> AzureSpeechTranslateSession:
        session_id = str(uuid.uuid4())
        new_session = AzureSpeechTranslateSession(self.user_id, self.db_manager, session_id, config)
        self.sessions[session_id] = new_session
        self.current_session = new_session
        return new_session
    
    def set_user_id(self, userid):
        self.user_id = userid
    
    def get_user_id(self) -> str:
        return self.user_id

    def get_sessions(self):
        pass
    
    def destroy_session(self):
        pass