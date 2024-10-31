import configparser
import json
import ast
import os
class UserSettings:
    def __init__(self):
        self.user_id = None
        self.default_detectable_languages = None # Language code plus locale, i.e. en-US
        self.default_speech_recognition_language = None # Language code plus locale, i.e. en-US
        self.default_source_language = None # Language code only
        self.default_target_language = None # Language code only
        self.audio_source = None 
        self.logged_in_status = False
        self.premium_status = None
        self.default_record_translations = None
        self.audio_source_video_conference = None
        self.audio_source_default_mic = None
        self.config = None
        self.ini_file = None  # Define the ini_file attribute
        
        # Set the ini file path and read the ini file
        self.set_ini_file_path()

        # Set the users settings from the ini file
        self.read_ini()

    def set_ini_file_path(self):
        self.config = configparser.ConfigParser()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ini_file = os.path.join(base_dir, 'settings.ini')

    def write_ini(self, section, field, value):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set(section, field, value)
        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def read_ini(self):
        try:
            self.config.read(self.ini_file)
            
            # Ensure the read operation was successful
            if not self.config.sections():
                raise Exception("Failed to read the ini file")

            # Language settings
            self.speech_detection_languages = ast.literal_eval(self.config.get('Language', 'default_speech_detection_languages', fallback='["en-US", "es-MX"]'))
            self.default_target_language = self.config.get('Language', 'default_target_language', fallback='English (United States)')
            self.default_source_language = self.config.get('Language', 'default_source_language', fallback='Spanish (Mexico)')
            self.default_speech_recognition_language = self.config.get('Language', 'default_speech_recognition_language', fallback='en-US')
            self.default_detectable_languages = ast.literal_eval(self.config.get('Language', 'default_detectable_languages', fallback='["en-US", "es-MX"]'))
            
            # Premium options
            self.premium_status = self.config.getboolean('Authentication', 'premium_status', fallback=True)
            
            # Translation
            self.default_record_translations = self.config.getboolean('Translation', 'default_record_translations', fallback=True)

            # Audio Source
            self.audio_source_video_conference = self.config.getboolean('Audio Source', 'audio_source_video_conference', fallback=True)
            self.audio_source_default_mic = self.config.getboolean('Audio Source', 'audio_source_default_mic', fallback=True)

            # Authentication
            self.logged_in_status = self.config.getboolean('Authentication', 'logged_in_status', fallback=True)

        except Exception as e:
            print(f"Error reading ini file: {e}")
    
    # Setters

    def set_audio_source(self, source):
        if source not in ["default", "video_conference"]:
            raise ValueError("Invalid audio source. Use 'default' or 'video_conference'.")
        
        self.audio_source_default_mic = (source == "default")
        self.audio_source_video_conference = (source == "video_conference")
        
        self.write_ini('Audio Source', 'audio_source_default_mic', str(self.audio_source_default_mic)) 
        self.write_ini('Audio Source', 'audio_source_video_conference', str(self.audio_source_video_conference))

    def set_default_record_translations(self, value):
        self.default_record_translations = value
        self.write_ini('Translation', 'default_record_translations', str(value))

    def set_default_detectable_languages(self, languages):
        print(languages)
        languages_str = json.dumps(languages)  # Convert list to JSON string
        self.write_ini('Language', 'default_detectable_languages', languages_str)

    def set_default_source_language(self, language): # This is the translation language code without the locale, i.e. es
        self.write_ini('Language', 'default_source_language', language)

    def set_default_target_language(self, language): # This is the translation language code without the locale, i.e. es
        self.write_ini('Language', 'default_target_language', language)
    
    def set_default_speech_detection_languages(self, languages):
        languages_str = json.dumps(languages)  # Convert list to JSON string
        self.write_ini('Language', 'default_speech_detection_languages', languages_str)
    
    def set_default_speech_recognition_language(self, languages):
        self.default_speech_recognition_language = languages
        self.write_ini('Language', 'default_speech_recognition_language', languages)
    
    def set_logged_in_status(self, status):
        self.logged_in_status = status
        self.write_ini('Authentication', 'logged_in_status', str(status))
    
    # TODO: Implement premium status from database
    def set_premium_status(self, status):
        self.premium_status = status
        self.write_ini('Authentication', 'premium_status', str(status))

    # Language Settings

    def get_language_code_from_locale(self, language_code):
        return self.language_options[language_code]
    
    def get_default_source_language(self):
        return self.default_source_language
    
    def get_default_target_language(self):
        return self.default_target_language
    
    def get_default_detectable_languages(self):
        return self.default_detectable_languages
    
    def get_default_speech_recognition_language(self):
        return self.default_speech_recognition_language
    
    # Auth Settings

    def get_logged_in_status(self):
        return self.logged_in_status
    
    def get_premium_status(self):
        return self.premium_status
    
    # Audio Sources

    def get_audio_source(self):
        if self.audio_source_default_mic:
            return "default"
        elif self.audio_source_video_conference:
            return "video_conference"
        else:
            return None  # or a default value if neither is True
    
    def is_logged_in(self):
        return self.logged_in_status