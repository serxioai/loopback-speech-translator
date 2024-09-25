import os
import azure.cognitiveservices.speech as speechsdk
import completed_speech_translation_buffer as completed_speech_translation_buffer
import partial_speech_translation_buffer as partial_speech_translation_buffer

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
        self.output_languages = None  
        self.input_languages = None
        self.source_language = None
        self.target_language = None
        self.detectable_languages = None  
        self.selected_audio_source = None
        self.partial_translation = partial_speech_translation_buffer.PartialSpeechTranslationBuffer()
        self.completed_translation_buffer = completed_speech_translation_buffer.CompletedSpeechTranslationBuffer()

    def set_azure_speech_settings(self, config_settings):
        self.languages = config_settings['translated_languages']
        self.output_languages = [lang for lang in config_settings['translated_languages'].values()] # format is ['en','es']
        self.input_languages = config_settings['translated_languages']['source']
        self.speech_recognition_language = config_settings['speech_rec_lang'] 
        self.detectable_languages = config_settings['detectable_lang']
        self.selected_audio_source = config_settings['audio_source']
        self.build_connection()

    def build_connection(self):
        self.speech_translation_config = self.init_speech_translation_config()
        self.audio_config = self.set_audio_source()
        self.auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=self.detectable_languages)
        self.translation_recognizer = self.init_translation_recognizer()
        self.completed_translation_buffer.init_buffer(self.output_languages)
        # TODO implement partial translation buffer
        self.set_event_callbacks()

    def init_speech_translation_config(self):
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=SUBSCRIPTION_KEY,
            region=SERVICE_REGION,
            speech_recognition_language= self.speech_recognition_language,
            target_languages= self.output_languages
            )

        # Start and stop continuous recognition with Continuous LID
        speech_translation_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

        return speech_translation_config
    
    def set_audio_source(self):
        if self.selected_audio_source == "blackhole":
            audio_config = speechsdk.audio.AudioConfig(device_name="BlackHole64ch_UID")
        elif self.selected_audio_source == "default":
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True) #Use use_default_mic for the bluetooth, choose Anker for the input device

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
            lambda evt: self.completed_result(evt))

        self.translation_recognizer.recognizing.connect(
            lambda evt: self.partial_result(evt))
                
        self.translation_recognizer.session_started.connect(
            lambda evt: self.session_started_result(evt))

        self.translation_recognizer.session_stopped.connect(
            lambda evt: self.session_stopped(evt))
        
        self.translation_recognizer.canceled.connect(
            lambda evt: self.canceled(evt))

        self.translation_recognizer.session_stopped.connect(
            lambda evt: self.session_stopped(evt))

    def get_source_language(self):
        return self.source_language
    
    def get_target_language(self):
        return self.target_language
    
    def get_output_languages(self):
        return self.output_languages
    
    def partial_result(self, evt):
        translations = evt.result.translations

        self.recognizing_event_counter += 1

        # Put the newest translation into the observable buffer
        for lang, text in translations.items():
            self.partial_translation.update(lang, text)     

    def completed_result(self, evt):
        translations = evt.result.translations
        if translations:
            self.completed_translation_buffer.update(translations)

    def canceled(self, evt):
        pass

    def reconnect(self):
        pass

    def start_streaming(self):
        self.translation_recognizer.start_continuous_recognition()
        print("start_streaming...")

    def stop_streaming(self):
        self.translation_recognizer.stop_continuous_recognition()

    def get_completed_translation_buffer(self):
        return self.completed_translation_buffer