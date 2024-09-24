

import azure.cognitiveservices.speech as speechsdk
import difflib

class CompleteSpeechTranslationBuffer:
    def __init__(self):
        self.buffer = None
      
    def init_buffer(self, languages):
        # Dictionary to hold the result from the recognized events
        self.buffer = {lang: [] for lang in languages}

    def update(self, language, translation):
        if language in self.buffer:
            self.buffer[language].append(translation)

    def get_source_translation(self, language):
        return self.buffer[language]

    def get_target_translation(self, language):
        return self.buffer[language]

   