from abc import ABC, abstractmethod
import difflib

class Observer(ABC):
    @abstractmethod
    def update_display(self, data, reason):
        pass 

class EventSignalBuffer:
    def __init__(self):
        self.buffer = {}
        self._observers = []

        # Temporary storage for the recognizing text output 
        self.observable_buffer = {}
        self.comparison_buffer = {}

        # Add a pointer dictionary to track the current item being processed/displayed for each language
        self.current_pointer = {}
        
    def init_buffer(self, languages):
            # Dictionary to hold the result from the recognized events
            self.buffer = {lang: [] for lang in languages}

    def update(self, translations, reason):
        if reason == "RECOGNIZING":
            for language, translation in translations.items():
                self.synthesize_recognizing_translation(language, translation)
                translation = self.get_next_synthesized_translation(language)
                self.buffer[language].append(translation)
                print("RECOGNIZING: {}".format(self.buffer))
        elif reason == "RECOGNIZED":
            self.buffer = {lang: [] for lang in self.buffer.keys()}
            for language, translation in translations.items():
                if language in self.buffer:
                    self.buffer[language].append(translation)   
                print("RECOGNIZED: {}".format(self.buffer))
        self._notify(reason)

    def attach(self, observer):
        self._observers.append(observer)

    def _notify(self, reason):
        for observer in self._observers:
            observer.update_display(self.buffer, reason)

    def synthesize_recognizing_translation(self, language_code, translation):
         # Check if language_code exists in the buffers
        if language_code not in self.observable_buffer:
            self.observable_buffer[language_code] = []
        if language_code not in self.comparison_buffer:
            self.comparison_buffer[language_code] = ''
        
        d = difflib.Differ()
        diff = list(d.compare(self.comparison_buffer[language_code], translation))
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
        self.comparison_buffer[language_code] = translation    

    def get_next_synthesized_translation(self, language_code):
        if language_code in self.observable_buffer and self.current_pointer[language_code] < len(self.observable_buffer[language_code]):
            translation = self.observable_buffer[language_code][self.current_pointer[language_code]]
            self.current_pointer[language_code] += 1
            return translation
        return None    