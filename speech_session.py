from dotenv import load_dotenv
import uuid
import os
from speech_api import SpeechAPI

# Load the .env file
load_dotenv()

SUBSCRIPTION_KEY = os.environ.get("SPEECH_KEY")
SPEECH_REGION = os.environ.get("SPEECH_REGION")

translationLanguages = ["es","en"]
source_language = "en"
target_language = "es"
speechRecognitionLanguage = "en-US"
detectableLanguages = ["en-US","es-MX"]
font = ("Arial", 22)
endSilenceTimeout = -1

class SpeechSession:
    def __init__(self, selected_audio_source, translation_languages, 
                 speech_recognition_language, detectable_languages):
        self.session_id = self.create_session_id()
        self.subscription_key = SUBSCRIPTION_KEY
        self.service_region = SPEECH_REGION
        self.translation_languages = translation_languages
        self.detectable_languages = detectable_languages
        self.selected_audio_source = selected_audio_source
        self.speech_recognition_language = speech_recognition_language
        self.speechAPI = None

        self.create_session_id()
        self.connect_azure_speech_api()

    def create_session_id(self) -> str:
        return str(uuid.uuid4())

    def start(self):
        # Start speech recognition or any other action you want
        print("Starting session...")
        self.clear_screen()

        # Set up the connection to Azure Speech
        self.speechAPI = SpeechAPI(subscription_key=self.subscription_key, 
                                   service_region=self.service_region, 
                                   translation_languages=translationLanguages, 
                                   speech_recognition_language=speechRecognitionLanguage, 
                                   detectable_languages=detectableLanguages,
                                   selected_audio_source=self.selected_audio_source)
        
        # Connect the buffers holding the event results
        self.speechAPI.set_recognized_callback(self.on_recognized_updated)
        self.speechAPI.set_recognizing_callback(self.on_recognizing_updated)
        self.speechAPI.configure_session()
        self.speechAPI.translation_recognizer.start_continuous_recognition()