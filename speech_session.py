from turtle import done
import azure.cognitiveservices.speech as speechsdk
import os
import time
import json
import queue
import difflib
import threading
import os

SUBSCRIPTION_KEY = os.environ.get("SPEECH_KEY")
SERVICE_REGION = os.environ.get("SPEECH_REGION")

class AzureSpeechTranslateSession:
    
    def __init__(self, session_id, config_data):
        self.session_id = session_id

        # Config data
        self.target_languages = config_data['target_languages']
        self.speech_recognition_language = "en-US" 
        self.detectable_languages = ["en-US", "es-MX"]
        self.selected_audio_source = config_data['audio_source']

        # Config setup
        self.speech_translation_config = None
        self.audio_config = None
        self.auto_detect_source_language_config = None
        self.translation_recognizer = None

        # Callbacks
        self.recognizing_event_speed = 0
        self.recognized_callback = None
        self.recognizing_callback = None
        self.recognizing_event_counter = 0
        self.recognizing_event_rate = 0

        # Dictionary to hold the result from the recognized events
        self.recognized_buffer = {lang: [] for lang in self.target_languages}
        
        # Storage the recognizing text output 
        self.observable_buffer = {}
        self.comparison_buffer = {}

        # Add a pointer dictionary to track the current item being processed/displayed for each language
        self.current_pointer = {}
        
    def start(self):
        if not self.translation_recognizer:
            raise ValueError("Translation recognizer is not initialized.")
        try:
            print(f"SESSION {self.session_id} STARTING...")
            self.translation_recognizer.start_continuous_recognition()
        except Exception as e:
            print("Failed to start recognition:", str(e))

    def stop(self):
        self.translation_recognizer.stop_continuous_recognition()

    def get_recognized_buffer(self):
        return self.recognized_buffer
    
    def configure(self):
        self.speech_translation_config = self.init_speech_translation_config()
        self.audio_config = self.set_audio_source()
        self.auto_detect_source_language_config = self.config_auto_detect_source_language()
        self.translation_recognizer = self.init_translation_recognizer()
        self.set_event_callbacks()

    # Step 1
    def init_speech_translation_config(self):
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=SUBSCRIPTION_KEY,
            region=SERVICE_REGION,
            speech_recognition_language= self.speech_recognition_language,
            target_languages= self.target_languages
            )
        
        # Start and stop continuous recognition with Continuous LID
        speech_translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

        return speech_translation_config
    
    def set_audio_source(self):
        if self.selected_audio_source == "headphones":
            audio_config = speechsdk.audio.AudioConfig(device_name="BlackHole16ch_UID")
        elif self.selected_audio_source == "default":
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True) #Use use_default_mic for the bluetooth, choose Anker for the input device

        return audio_config
    
    def config_auto_detect_source_language(self):
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(self.detectable_languages)
        return auto_detect_source_language_config
    
    def init_translation_recognizer(self) -> speechsdk.translation.TranslationRecognizer:
        translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.speech_translation_config,
            audio_config=self.audio_config,
            auto_detect_source_language_config=self.auto_detect_source_language_config)
        return translation_recognizer
        
    def trigger_recognized_event(self):
        time.sleep(1)
    
    def set_recognizing_event_counter(self, count: int) -> None:
        self.recognizing_event_counter = count

    def get_recognizing_event_counter(self) -> int:
        return self.recognizing_event_counter
    
    def get_session_id(self) -> str:
        return self.get_session_id
    
    def get_speech_recognition_language(self) -> str:
        return self.speech_recognition_language
    
    def get_target_languages(self) -> tuple[str, str]:
        return self.target_languages

    def set_recognizing_event_rate(self, rate):    
        self.recognizing_event_rate = rate
    
    def get_recognizing_event_rate(self):
        return self.recognizing_event_rate
    
    def set_event_callbacks(self):

        self.translation_recognizer.recognized.connect(
            lambda evt: self.result_callback('RECOGNIZED', evt))

        self.translation_recognizer.recognizing.connect(
            lambda evt: self.result_callback('RECOGNIZING', evt))
                
        self.translation_recognizer.session_started.connect(
            lambda evt: self.result_callback('SESSION STARTED', evt))

        self.translation_recognizer.session_stopped.connect(
            lambda evt: print('SESSION STOPPED {}'.format(evt)))
            
        self.translation_recognizer.canceled.connect(
            lambda evt: print('CANCELED: {} ({})'.format(evt, evt.reason)))

        self.translation_recognizer.session_stopped.connect(self.stop_cb)

        self.translation_recognizer.canceled.connect(self.stop_cb)
 
    def set_recognized_callback(self, callback):
        self.recognized_callback = callback
    
    def set_recognizing_callback(self, callback):
        self.recognizing_callback = callback

    def set_recognizing_event_counter(self, counter):
        self.recognizing_evnet_counter = counter
        
    # Update the buffers with the event type text and notify observers
    def result_callback(self, event_type, evt):
        
        translations = evt.result.translations

        # If translations dictionary is empty, return early
        if not translations:
            return
      
        if event_type == "RECOGNIZING":
            self.recognizing_event_counter += 1

            # Put the newest translation into the observable buffer
            for lang, text in translations.items():
                self.update_recognizing_translation(lang, text)        

            # Notify the observer the buffer has been updated
            if self.recognizing_event_rate == 0 or self.recognizing_event_counter % self.recognizing_event_rate == 0:
                self.recognizing_callback()

        elif event_type == "RECOGNIZED":

            for lang, text in translations.items():
                self.update_recognized_translation(lang, text)
            
            self.recognized_callback()

    def get_translation_recognizer(self):
        return self.translation_recognizer

    def reset_translation_recognizer(self):
        self.translation_recognizer = None

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        done = True
    
    # This is a final rendering
    def update_recognized_translation(self, language, translation):
        if language in self.recognized_buffer:
            self.recognized_buffer[language].append(translation)

    # Fill the buffer with the translations
    def update_recognizing_translation(self, language_code, current_transcription):
        
        # Check if language_code exists in the buffers
        if language_code not in self.observable_buffer:
            self.observable_buffer[language_code] = []
        if language_code not in self.comparison_buffer:
            self.comparison_buffer[language_code] = ''
        
        d = difflib.Differ()
        diff = list(d.compare(self.comparison_buffer[language_code], current_transcription))
        temp_observable = []
        addition = False

        for line in diff:
            # Check if it's an addition
            if line.startswith('+ '):
                addition = True
                temp_observable.append('+')
                temp_observable.append(line[2:])
            # Check if it's a common element (neither addition nor deletion)
            elif line.startswith('  '):
                if addition:
                    # Add a space before the next word if the previous one was an addition
                    temp_observable.append(' ')
                temp_observable.append(line[2:])
                addition = False
            # For deletions, skip
            else:
                continue

        # Append the observable for the language in the observable_buffer to maintain backlog
        self.observable_buffer[language_code].append(''.join(temp_observable))

        # If this language code is not in current_pointer, initialize it
        if language_code not in self.current_pointer:
            self.current_pointer[language_code] = 0

        # Update the comparison_buffer for the language
        self.comparison_buffer[language_code] = current_transcription

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

    def save_translations(self):
        pass


