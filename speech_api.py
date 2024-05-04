from turtle import done
import azure.cognitiveservices.speech as speechsdk
import os
import time
import json
import queue
import difflib
import threading

class SpeechAPI:

    def __init__(self, subscription_key, service_region, translation_languages, 
                 speech_recognition_language, detectable_languages, selected_audio_source):
        self.subscription_key = subscription_key
        self.service_region = service_region
        self.translation_languages = translation_languages
        self.speech_recognition_language = speech_recognition_language 
        self.detectable_languages = detectable_languages
        self.selected_audio_source = selected_audio_source
        self.speech_translation_config = self.set_speech_translation_config()
        self.audio_config = self.set_audio_config()
        self.auto_detect_source_language_config = self.set_auto_detect_source_language_config()
        self.translation_recognizer = None
        self.recognizing_event_speed = 0
        self.recognized_callback = None
        self.recognizing_callback = None
        self.recognizing_event_counter = 0
        self.recognizing_event_rate = 0
        
        self.done = False
        
        # Dictionary to hold the result from the recognized events
        self.recognized_buffer = {lang: [] for lang in self.translation_languages}
        
        # Storage the recognizing text output 
        self.observable_buffer = {}
        self.comparison_buffer = {}

        # Add a pointer dictionary to track the current item being processed/displayed for each language
        self.current_pointer = {}
        
    def get_recognized_buffer(self):
        return self.recognized_buffer
    
    def configure_session(self):
        self.set_translation_recognizer()
        self.set_event_callbacks()

    def trigger_recognized_event(self):
        time.sleep(1)
    
    def set_recognizing_event_counter(self, count: int) -> None:
        self.recognizing_event_counter = count

    def get_recognizing_event_counter(self) -> int:
        return self.recognizing_event_counter

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
                if self.recognizing_callback:
                    self.recognizing_callback()

        elif event_type == "RECOGNIZED":

            for lang, text in translations.items():
                self.update_recognized_translation(lang, text)
            
            if self.recognized_callback:
                self.recognized_callback()

    def get_translation_recognizer(self):
        return self.translation_recognizer

    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-identification?tabs=once&pivots=programming-language-python
    def set_speech_translation_config(self):
   
        # Fills the constructor for a translator recognizer with given settings
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=self.subscription_key,
            region=self.service_region,
            speech_recognition_language=self.speech_recognition_language,
            target_languages= self.translation_languages)
        
        # Start and stop continuous recognition with Continuous LID
        speech_translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

        return speech_translation_config

    def set_audio_config(self):
        if self.selected_audio_source == "headphones":
            audio_config = speechsdk.audio.AudioConfig(device_name="BlackHole16ch_UID")
        elif self.selected_audio_source == "default":
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True) #Use use_default_mic for the bluetooth, choose Anker for the input device

        return audio_config
    
    def set_auto_detect_source_language_config(self):
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(self.detectable_languages)
        return auto_detect_source_language_config

    def set_translation_recognizer(self):
        self.translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.speech_translation_config,
            audio_config=self.audio_config,
            auto_detect_source_language_config=self.auto_detect_source_language_config)

    def reset_translation_recognizer(self):
        self.translation_recognizer = None

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        #nonlocal done
        done = True
    
    # This is a final rendering
    def update_recognized_translation(self, language, translation):
        if language in self.recognized_buffer:
            self.recognized_buffer[language].append(translation)

    # This is a partial rendering of the time series 
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

    



