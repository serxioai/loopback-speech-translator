from turtle import done
import azure.cognitiveservices.speech as speechsdk
import os
import time
import json
import queue
import difflib
import threading
import os
import uuid
from azure_speech_config import AzureSpeechConfig

class AzureSpeechTranslateAPI:
    def __init__(self, user_id, db_manager):
        self.user_id = user_id
        self.db_manager = db_manager
        self.azure_speech_config = AzureSpeechConfig()

    def start_streaming(self, encoded_session_data):
        self.azure_speech_config.set_azure_speech_settings(encoded_session_data)
        self.azure_speech_config.start_streaming()

    def stop_streaming(self):
        self.azure_speech_config.stop_streaming()

    def get_session_id(self) -> str:
        return self.get_session_id

    def get_recognizing_event_buffer(self):
        return self.azure_speech_config.recognizing_event_buffer

    def get_recognized_event_buffer(self):
        return self.azure_speech_config.recognized_event_buffer

    def detect_language(self, evt):

        result = evt.result 
        print("Properties available:", result.properties.get(speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult)) 

        # Check if the result has the property for auto-detected language
        if result.properties.get(speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult):
            detected_language_json = result.properties[speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
            detected_language = speechsdk.AutoDetectSourceLanguageResult(detected_language_json).language
            print(f"Detected Language: {detected_language}")
        else:
            print("No language detected.")
        
    def get_translation_recognizer(self):
        return self.translation_recognizer

    def reset_translation_recognizer(self):
        self.translation_recognizer = None

    def on_canceled(self, args):
        print(f"Canceled: {args.reason}")
        if args.reason == speechsdk.CancellationReason.Error and self.should_reconnect:
            print("Error during session, attempting to reconnect...")
            self.connect()

    def save_translations(self, timestamp, input_transcription, output_translation):

        try:
            self.db_manager.translations.insert_one({
                "user_id": self.user_id,
                "session_id": self.session_id,
                "timestamp": timestamp,
                "in": input_transcription,
                "out": output_translation,
            })
            return True
        except Exception as e:
            print(f"Failed to save translation: {e}")
            return False