from datetime import datetime

class User:
    def __init__(self, user_id, email, username, password_hash, roles, created_at=None):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.roles = roles
        self.created_at = created_at or datetime.utcnow()
        self.last_login = None
        self.preferences = {}
        self.security_question = None
        self.security_answer = None
        self.login_history = []

    def update_last_login(self):
        """Update the last login timestamp to the current time."""
        self.last_login = datetime.utcnow()

    def set_preferences(self, preferences):
        """Set user preferences."""
        self.preferences = preferences

    def add_login_history(self, ip_address):
        """Log a login attempt with the current timestamp and IP address."""
        self.login_history.append({
            "timestamp": datetime.utcnow(),
            "ip_address": ip_address
        })

    def set_security_question(self, question, answer):
        """Set the user's security question and answer."""
        self.security_question = question
        self.security_answer = answer

    def check_password(self, password):
        """Check if the provided password matches the stored password hash."""
        # Implement password checking logic (e.g., using bcrypt)
        pass

    def to_dict(self):
        """Convert the user object to a dictionary for easy serialization."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "roles": self.roles,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "preferences": self.preferences,
            "security_question": self.security_question,
            "login_history": self.login_history
        }