from abc import ABC, abstractmethod
import difflib

class RecognizingBufferObserver(ABC):
    @abstractmethod
    def update_recognizing_event_display(self, buffer_content):
        pass 

class RecognizingEventSignalBuffer:
    def __init__(self):
        self._observers = []
        self.buffer = {}

        # Storage for the recognizing text synthesis and comparison
        self.observable_buffer = {}
        self.comparison_buffer = {}

        # Add a pointer dictionary to track the current item being processed/displayed for each language
        self.current_pointer = {}
        
    def init_buffer(self, languages):
        # Dictionaries for recognizing event processing
        self.current_pointer = {lang: 0 for lang in languages}
        self.observable_buffer = {lang: [] for lang in languages}
        self.comparison_buffer = {lang: '' for lang in languages}

    def update(self, translations_dict):
        output_dict = self.synthesize_recognizing_translations(translations_dict)
        for lang, translation in output_dict.items():
            if lang not in self.buffer:
                self.buffer[lang] = []
            if translation:
                self.buffer[lang] = translation
                #self.buffer[lang].append(translation)
        self._notify()

    def attach(self, observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update_recognizing_event_display(self.buffer)

    def synthesize_recognizing_translations(self, input_dict):
        output_dict = {}
        for language_code, current_transcription in input_dict.items():
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

            # Join the observable to form the updated translation
            updated_translation = ''.join(temp_observable)
            output_dict[language_code] = updated_translation

            # Append the observable for the language in the observable_buffer to maintain backlog
            self.observable_buffer[language_code].append(updated_translation)

            # If this language code is not in current_pointer, initialize it
            if language_code not in self.current_pointer:
                self.current_pointer[language_code] = 0

            # Update the comparison_buffer for the language
            self.comparison_buffer[language_code] = current_transcription

            # Retrieve the correct segment from the observable buffer
            if self.current_pointer[language_code] < len(self.observable_buffer[language_code]):
                translation = self.observable_buffer[language_code][self.current_pointer[language_code]]
                self.current_pointer[language_code] += 1
                output_dict[language_code] = translation

        return output_dict  