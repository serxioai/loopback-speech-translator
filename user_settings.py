import configparser
import json
import ast
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
        self.ini_file = 'settings.ini'  # Define the ini_file attribute
        self.config = configparser.ConfigParser()
        self.read_ini()

    def write_ini(self, field, value):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set('Settings', field, value)
        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def read_ini(self):
        try:
            self.config.read(self.ini_file)
            
            # Ensure the read operation was successful
            if not self.config.sections():
                raise Exception("Failed to read the ini file")

            # Extract settings
            self.speech_detection_languages = ast.literal_eval(self.config.get('Settings', 'default_speech_detection_languages', fallback='["en-US", "es-MX"]'))
            self.audio_source = self.config.get('Settings', 'audio_source', fallback='blackhole')
            self.default_target_language = self.config.get('Settings', 'default_target_language', fallback='English (United States)')
            self.logged_in_status = self.config.getboolean('Settings', 'logged_in_status', fallback=True)
            self.default_source_language = self.config.get('Settings', 'default_source_language', fallback='Spanish (Mexico)')
            self.default_speech_recognition_language = self.config.get('Settings', 'default_speech_recognition_language', fallback='en-US')
            self.default_detectable_languages = ast.literal_eval(self.config.get('Settings', 'default_detectable_languages', fallback='["en-US", "es-MX"]'))
            self.default_record_translations = self.config.getboolean('Settings', 'default_record_translations', fallback=True)
            self.premium_status = self.config.getboolean('Settings', 'premium_status', fallback=True)

        except Exception as e:
            print(f"Error reading ini file: {e}")
    
    # Setters
    def set_default_record_translations(self, value):
        self.default_record_translations = value
        self.write_ini('default_record_translations', str(value))

    def set_default_detectable_languages(self, languages):
        languages_str = json.dumps(languages)  # Convert list to JSON string
        self.write_ini('default_detectable_languages', languages_str)

    def set_default_source_language(self, language): # This is the translation language code without the locale, i.e. es
        self.write_ini('default_source_language', language)

    def set_default_target_language(self, language): # This is the translation language code without the locale, i.e. es
        self.write_ini('default_target_language', language)
    
    def set_default_speech_detection_languages(self, languages):
        languages_str = json.dumps(languages)  # Convert list to JSON string
        self.write_ini('default_speech_detection_languages', languages_str)
    
    def set_default_speech_recognition_language(self, languages):
        self.default_speech_recognition_language = languages
        self.write_ini('default_speech_recognition_language', languages)
    
    def set_audio_source(self, source):
        self.audio_source = source
        self.write_ini('audio_source', source)
    
    def set_logged_in_status(self, status):
        self.logged_in_status = status
        self.write_ini('logged_in_status', str(status))
    
    def set_premium_status(self, status):
        self.premium_status = status
        self.write_ini('premium_status', str(status))

    # Getters

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
    
    def get_audio_source(self):
        return self.audio_source
    
    def get_logged_in_status(self):
        return self.logged_in_status
    
    def get_premium_status(self):
        return self.premium_status

