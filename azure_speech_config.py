
import os
import azure.cognitiveservices.speech as speechsdk

SUBSCRIPTION_KEY = os.environ.get("AZURE_KEY")
SERVICE_REGION = os.environ.get("AZURE_REGION")

class AzureSpeechConfig:
    def __init__(self):
        self.speech_translation_config = None
        self.audio_config = None
        self.auto_detect_source_language_config = None
        self.translation_recognizer = None
        self.translated_languages = None
        self.speech_recognition_language = None
        
    def set_azure_speech_config(self, config_settings):
        self.languages = config_settings['languages']
        self.output_languages = [lang for lang in config_settings['languages'].values()] # format is ['en','es']
        self.input_languages = config_settings['languages']['source']
        self.speech_recognition_language = config_settings['speech_rec_lang'] 
        self.detectable_languages = config_settings['detectable_lang']
        self.selected_audio_source = config_settings['audio_source']

        self.config()

    def configure(self):
        self.speech_translation_config = self.init_speech_translation_config()
        self.audio_config = self.set_audio_source()
        self.auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(self.detectable_languages)
        #print("Detectable languages set in AutoDetectSourceLanguageConfig:")
        #print(self.auto_detect_source_language_config.language)
        self.translation_recognizer = self.init_translation_recognizer()
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
        if self.selected_audio_source == "headphones":
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
    
    def set_event_callbacks(self):
        
        self.translation_recognizer.recognized.connect(
            lambda evt: self.result_callback('RECOGNIZED', evt))

        self.translation_recognizer.recognizing.connect(
            lambda evt: self.result_callback('RECOGNIZING', evt))
                
        self.translation_recognizer.session_started.connect(
            lambda evt: self.result_callback('SESSION STARTED', evt))

        self.translation_recognizer.session_stopped.connect(
            lambda evt: print('SESSION STOPPED {}'.format(evt)))
        
        self.translation_recognizer.canceled.connect(self.on_canceled)

        self.translation_recognizer.session_stopped.connect(self.stop)

    def get_output_languages(self):
        return self.output_languages
