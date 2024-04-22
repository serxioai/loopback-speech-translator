import threading
import time

class WordsPerMinute:
    def __init__(self, recognized_buffer):
        self.words_per_minute = 0
        self.buffer = recognized_buffer
    
    def get_words_per_minute(self):
        return self.words_per_minute
    
    def start_polling_recognized_buffer_length(self):
        # Create and start a thread for polling recognized text length
        self.polling_thread = threading.Thread(target=self.poll_recognized_buffer_length)
        self.polling_thread.daemon = True  # Set as daemon so it stops when the main thread stops
        self.polling_thread.start()
    
    def poll_recognized_buffer_length(self):
        while True:
            # recognized_text_length = {lang: len(buffer) for lang, buffer in self.recognized_buffer.items()}
            source_temp_buffer = self.recognized_buffer[self.translation_languages[0]]
            # print(source_temp_buffer)
            # print(f"total words: {total_words}")
            time.sleep(10)

    def calculate_words_per_minute(self, recognized_text):
        # Split the recognized text into words
        words = recognized_text.split()
        
        # Update total word count
        total_words += len(words)

        # Calculate time elapsed
        current_time = time.time()
        time_elased = current_time - self.start_time

        # Calculate wpm
        if time_elased > 0:
            self.words_per_minute = (total_words / time_elased) * 60
        else:
            self.words_per_minute = 0