from abc import ABC, abstractmethod

class RecognizedBufferObserver(ABC):
    @abstractmethod
    def update_recognized_event_display(self, buffer_content):
        pass

class RecognizedEventSignalBuffer():
    def __init__(self):
        self._observers = []
        self.buffer = {}

    def init_buffer(self, languages):
        self.buffer = {lang: [] for lang in languages}

    def update(self, translation_dict):
        for lang, translation in translation_dict.items():
            self.buffer[lang].append(translation)
        self._notify()

    def attach(self, observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update_recognized_event_display(self.buffer)

