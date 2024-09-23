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
from azure_translation_buffer import AzureTranslationBuffer

class AzureSpeechTranslateAPI:
    
    def __init__(self, 
                 user_id, 
                 db_manager,
                 recognized_callback,
            ):
        self.user_id = user_id
        self.db_manager = db_manager
        self.azure_speech_config = AzureSpeechConfig()
        self.azure_translation_buffer = AzureTranslationBuffer()
        self.recognized_callback = recognized_callback
    
    def set_config(self, config_data):
        self.azure_speech_config.set_azure_speech_config(config_data)

    def start_streaming(self, encoded_session_data):
        self.set_config(encoded_session_data)
        self.azure_translation_buffer.init_recognized_buffer(encoded_session_data)

        if not self.azure_speech_config.translation_recognizer:
            raise ValueError("Translation recognizer is not initialized.")
        try:
            print(f"SESSION {self.session_id} STARTING...")
            self.azure_speech_config.translation_recognizer.start_continuous_recognition()
        except Exception as e:
            print("Failed to start recognition:", str(e))

    def stop_streaming(self):
        self.azure_speech_config.translation_recognizer.stop_continuous_recognition()

    def reconnect(self):
        pass

    def get_recognized_buffer(self):
        return self.recognized_buffer
    
    def get_languages(self):
        return self.azure_speech_config.languages
    
    def get_session_id(self) -> str:
        return self.get_session_id
    
    def get_speech_recognition_language(self) -> str:
        return self.azure_speech_config.speech_recognition_language
    
    def get_output_languages(self) -> tuple[str, str]:
        return self.azure_speech_config.output_languages
    
    def set_recognized_callback(self, callback):
        self.recognized_callback = callback
    
    def set_recognizing_callback(self, callback):
        self.recognizing_callback = callback

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
        

    # Update the buffers with the event type text and notify observers
    def result_callback(self, event_type, evt):

        # TODO: implement language detection
        
        translations = evt.result.translations
        # print(translations)
        # If translations dictionary is empty, return early
        if not translations:
            return
      
        if event_type == "RECOGNIZING":
            self.recognizing_event_counter += 1
            # Put the newest translation into the observable buffer
            for lang, text in translations.items():
                self.update_recognizing_translation(lang, text)        

        elif event_type == "RECOGNIZED":
            for lang, text in translations.items():
                self.update_recognized_translation(lang, text)
            
            self.recognized_callback()

    def get_translation_recognizer(self):
        return self.translation_recognizer

    def reset_translation_recognizer(self):
        self.translation_recognizer = None

    def on_canceled(self, args):
        print(f"Canceled: {args.reason}")
        if args.reason == speechsdk.CancellationReason.Error and self.should_reconnect:
            print("Error during session, attempting to reconnect...")
            self.connect()
    
    
    def get_next_transcription(self, language_code):
        if language_code in self.observable_buffer and self.current_pointer[language_code] < len(self.observable_buffer[language_code]):
            transcription = self.observable_buffer[language_code][self.current_pointer[language_code]]
            self.current_pointer[language_code] += 1
            return transcription
        return None

    def get_recognized_translations(self, language):
        translations = self.recognized_buffer.get(language, [""])
        return translations[-1] if translations else ""
    
    def get_recognizing_translations(self, language):
        translations = self.observable_buffer.get(language, [""])
        return translations if translations else ""

    def set_recognized_translation(self, language, translation):
            if language in self.buffers:
                self.recognized_buffer[language] = [translation]

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