from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass 

class CompletedSpeechTranslationBuffer:
    def __init__(self):
        self.buffer = {}
        self._observers = []
      
    def init_buffer(self, languages):
        # Dictionary to hold the result from the recognized events
        self.buffer = {lang: [] for lang in languages}

    def update(self, translations):
        for language, translation in translations.items():
            if language in self.buffer:
                self.buffer[language].append(translation)
        
        self._notify()

    def get_source_translation(self, language):
        return self.buffer[language]

    def get_target_translation(self, language):
        return self.buffer[language]

    # Method to register an observer
    def attach(self, observer):
        self._observers.append(observer)

    # Method to unregister an observer
    def detach(self, observer):
        self._observers.remove(observer)

    # Method to notify all observers
    def _notify(self):
        for observer in self._observers:
            observer.update(self.buffer)

