import difflib

class PartialSpeechTranslationSegment:
    def __init__(self):
        self.recognizing_buffer = None
        
        # Counter to keep track of the number of recognizing events
        self.recognizing_event_counter = 0
        
        # Storage the recognizing text output 
        self.observable_buffer = {}
        self.comparison_buffer = {}

        # Add a pointer dictionary to track the current item being processed/displayed for each language
        self.current_pointer = {}

     # Fill the buffer with the translations
    def update(self, language_code, current_transcription):
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

    def set_recognizing_event_counter(self, count: int) -> None:
        self.recognizing_event_counter = count
    
    def get_recognizing_event_counter(self) -> int:
        return self.recognizing_event_counter