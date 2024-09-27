from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass 

class EventSignalBuffer:
    def __init__(self):
        self.buffer = {}
        self._observers = []
        
        self.recognizing_event_counter = 0
        
    def init_buffer(self, languages):
            # Dictionary to hold the result from the recognized events
            self.buffer = {lang: [] for lang in languages}

    def update(self, translations, reason):
        if reason == "RECOGNIZING":
            for language, translation in translations.items():
                
                if language in self.buffer:
                    self.buffer[language].append(translation)
                    print("RECOGNIZING BUFFER:", self.buffer)
        elif reason == "RECOGNIZED":
            for language, translation in translations.items():
                if language in self.buffer:
                    self.buffer[language].append(translation)   
                    print("RECOGNIZED BUFFER:", self.buffer)
            
        self._notify()

    def attach(self, observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self.buffer)