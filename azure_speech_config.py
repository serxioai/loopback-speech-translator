import os
import azure.cognitiveservices.speech as speechsdk
import recognizing_event_signal_buffer as recognizing_event_signal_buffer
import recognized_event_signal_buffer as recognized_event_signal_buffer

SUBSCRIPTION_KEY = os.environ.get("AZURE_KEY")
SERVICE_REGION = os.environ.get("AZURE_REGION")

class AzureSpeechConfig:
    def __init__(self):
        self.recognized_callback = None
        self.speech_translation_config = None
        self.audio_config = None
        self.auto_detect_source_language_config = None
        self.translation_recognizer = None
        self.translated_languages = None
        self.speech_recognition_language = None
        self.languages = None  
        self.source_language = None
        self.target_language = None
        self.detectable_languages = None  
        self.selected_audio_source = None
        
        # Buffers for recognizing and recognized events
        self.recognizing_event_buffer = recognizing_event_signal_buffer.RecognizingEventSignalBuffer()
        self.recognized_event_buffer = recognized_event_signal_buffer.RecognizedEventSignalBuffer()

    def set_azure_speech_settings(self, config_settings):
        self.translated_languages = config_settings['session_languages'] # The UI shows source as the translated language
        self.speech_recognition_language = config_settings['speech_rec_lang']        
        self.detectable_languages = config_settings['detectable_lang']
        self.selected_audio_source = config_settings['audio_source']
        self.build_connection()

    def build_connection(self):
        self.speech_translation_config = self.init_speech_translation_config()
        self.audio_config = self.set_audio_source()
        self.auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=self.detectable_languages)
        self.translation_recognizer = self.init_translation_recognizer()
        
        # Initialize the buffers for the source and target languages
        self.recognizing_event_buffer.init_buffer(self.translated_languages)
        self.recognized_event_buffer.init_buffer(self.translated_languages)
        
        # Set the event callbacks for the translation recognizer
        self.set_event_callbacks()

    def init_speech_translation_config(self):
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=SUBSCRIPTION_KEY,
            region=SERVICE_REGION,
            speech_recognition_language=self.speech_recognition_language,
            target_languages=self.translated_languages
            )

        # Start and stop continuous recognition with Continuous LID
        speech_translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

        return speech_translation_config
    
    def set_audio_source(self):
        try:
            if self.selected_audio_source == "video_conference":
                audio_config = speechsdk.audio.AudioConfig(device_name="BlackHole64ch_UID")
            elif self.selected_audio_source == "default":
                audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True) #Use use_default_mic for the bluetooth, choose Anker for the input device
            else:
                raise ValueError(f"Invalid audio source: {self.selected_audio_source}")
        except Exception as e:
            print(f"Error setting audio source: {e}")
            audio_config = None

        return audio_config
        
    def init_translation_recognizer(self) -> speechsdk.translation.TranslationRecognizer:
        translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.speech_translation_config,
            audio_config=self.audio_config,
            auto_detect_source_language_config=self.auto_detect_source_language_config)
        return translation_recognizer

    def set_complete_translation_view_callback(self, callback):
        self.complete_translation_view_callback = callback

    def set_event_callbacks(self):
        
        self.translation_recognizer.recognized.connect(
            lambda evt: self.update_event_signal_recognized(evt))

        self.translation_recognizer.recognizing.connect(
            lambda evt: self.update_event_signal_recognizing(evt))
        
        self.translation_recognizer.session_started.connect(
            lambda evt: self.start(evt))

        self.translation_recognizer.session_stopped.connect(
            lambda evt: self.stopped(evt))
        
        self.translation_recognizer.canceled.connect(
            lambda evt: self.canceled(evt))
    
    def update_event_signal_recognizing(self, evt):
        translation_dict = evt.result.translations 
        print(f"Recognizing: {translation_dict}")
        self.recognizing_event_buffer.update(translation_dict)  

    def update_event_signal_recognized(self, evt):
        translation_dict = evt.result.translations
        self.recognized_event_buffer.update(translation_dict)

    def start(self, evt):
        print("SESSION STARTED {}".format(evt))

    def stopped(self, evt):
        print("SESSION STOPPED {}".format(evt))

    def canceled(self, evt):
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Canceled: {evt.reason}")
            print("SESSION STOPPED {}".format(evt))
            self.reconnect()

    def reconnect(self):
        print("Attempting to reconnect...")
        try:
            self.translation_recognizer.stop_continuous_recognition_async()
            self.translation_recognizer.start_continuous_recognition_async()
            print("Reconnected successfully.")
        except Exception as e:
            print(f"Reconnection failed: {e}")

    def start_streaming(self):
        self.translation_recognizer.start_continuous_recognition_async()

    def stop_streaming(self):
        self.translation_recognizer.stop_continuous_recognition_async()

