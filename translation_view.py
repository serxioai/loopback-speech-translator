# translation_view.py

import tkinter as tk
from tkinter import font as tkfont
import time

class TranslationView(tk.Frame):
    def __init__(self, 
                 current_session, 
                 root, 
                 on_start_speech_session_callback,
                 on_stop_speech_session_callback,
                 on_change_recognizing_event_rate_callback):
        super().__init__(root)
        self.root = root
        self.current_session = current_session
        self.on_change_recognizing_event_rate_callback = on_change_recognizing_event_rate_callback
        self.on_start_speech_session_callback = on_start_speech_session_callback
        self.on_stop_speech_session_callback = on_stop_speech_session_callback
        self.grid(sticky="nsew")

        # Ensure the frame expands
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
 
        self.build_ui()

        self.current_session.set_recognizing_callback(self.on_recognizing_updated)
        self.current_session.set_recognized_callback(self.on_recognized_updated)
       
    def build_ui(self):
        
       # Define the font
        font = tkfont.Font(family="Helvetica", size=15)

        # Configure grid weights for the main frame
        # self.grid_columnconfigure(0, weight=3)  # Left column (3/5)
        # self.grid_columnconfigure(1, weight=2)  # Right column (2/5)

        # 1/2
        self.grid_columnconfigure(0, weight=3)  # Left column (3/5)
        self.grid_columnconfigure(1, weight=2)  # Right column (3/5)

        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=0)  # Bottom row

        # Setup the viewing windows for recognized and recognizing events
        self.translated_language = tk.Text(self, bg="white", font=font) # This is the language with RECOGNIZING status
        self.detected_language = tk.Text(self, bg="white", font=font) # This is a hybrid of RECOGNIZING and RECOGNIZED

        # Place the text widgets in the frames
        self.detected_language.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.translated_language.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)

        # Add a bar at the bottom
        self.bottom_bar = tk.Frame(self)
        self.bottom_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Add "Start" and "Stop" buttons to the bottom bar
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.on_start_speech_session_callback)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.on_stop_speech_session_callback)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

        # Add a slider below the receiving text widget in the right frame
        self.recognizing_rate_slider = tk.Scale(self.bottom_bar, from_=0, to=8, orient='horizontal', label='Recognizing Event Rate')
        self.recognizing_rate_slider.pack(side=tk.RIGHT, padx=10, pady=5)
        self.recognizing_rate_slider.set(0)
        self.recognizing_rate_slider.bind("<Motion>", lambda event: self.on_change_recognizing_event_rate_callback(self.recognizing_rate_slider.get()))
        
    def clear_screen(self):
        self.translated_language.delete(1.0, tk.END)
        self.detected_language.delete(1.0, tk.END)

    def update_recognized_texts(self, recognized_source, recognized_target):
        # detected_language_code = self.current_session.get_detected_language()

        current_time = time.strftime("%H:%M:%S")  # Get current time
        #timestamped_source = f"{current_time} {detected_language_code} - {recognized_source}"
        #timestamped_target = f"{current_time} {detected_language_code}- {recognized_target}"

        timestamped_source = f"{current_time} - {recognized_source}"
        timestamped_target = f"{current_time} - {recognized_target}"

        # print("Timestamped source: ", timestamped_source)
        # Insert the timestamped texts at the beginning of the text widget
        self.detected_language.insert("1.0", timestamped_source + "\n\n")
        self.detected_language.insert("1.0", timestamped_target + "\n\n")

        # Highlight the newly inserted text
        self.highlight_text(self.recognized_text_source)
        self.highlight_text(self.recognized_text_target)

    # Update the screen with the contents of the observable buffer
    def update_recognizing_texts(self, recognizing_source, recognizing_target):
       # self.recognizing_text_source.delete(1.0, tk.END)
       # self.recognizing_text_source.insert(tk.END, recognizing_source + "\n\n")
        self.recognizing_text_target.delete(1.0,tk.END)
        self.recognizing_text_target.insert(tk.END, recognizing_target + "\n\n")

    def highlight_text(self, text_widget):
        # Get the index of the newly inserted text
        start_index = text_widget.index("1.0")
        end_index = text_widget.index("2.0")
        
        # Apply a pale blue background color to the newly inserted text
        text_widget.tag_add("highlight", start_index, end_index)
        text_widget.tag_configure("highlight", background="#C9E2FF")  # Pale blue color

        # Schedule a function to remove the highlight after 1 second
        self.after(1000, lambda: self.remove_highlight(text_widget))

    def remove_highlight(self, text_widget):
        # Remove the highlight from the text
        text_widget.tag_remove("highlight", "1.0", "end")

    # Callback method for the observer
    def on_recognized_updated(self):
        for index, lang in enumerate(self.session.target_languages):
            if index == 0:    
                self.detected_language = self.session.get_recognized_translations(lang)
            if index == 1:
                self.detected_language = self.session.get_recognized_translations(lang)

        # Update the UI with translations
        self.update_recognized_texts(recognized_text_source, recognized_text_target)

    def on_recognizing_updated(self):
        # Iterate through each language code in the list
        for index, language_code in enumerate(self.current_session.target_languages):

            # Call display_text with the current language code
            if index == 0:
                self.display_recognizing_text(language_code, self.translated_language)
            if index == 1:
                self.display_recognizing_text(language_code, self.translated_language)

    def display_recognizing_text(self, language, text_widget):
        # Clear the text widget
        text_widget.delete(1.0, tk.END)

        # Fetch translations for the given language
        translations = self.current_session.get_next_transcription(language)
        i = 0
        while i < len(translations):
            if translations[i] == '+' and i < len(translations) - 1:
                # Insert the next character after '+'
                text_widget.insert(tk.END, translations[i + 1])
                # Highlight the character
                text_widget.tag_add("highlight", f"{tk.END} - 2c", tk.END)
                i += 2  # Move past the '+' and the character
            else:
                # Insert other characters normally
                text_widget.insert(tk.END, translations[i])
                i += 1

        # Highlight text setup (if not already configured elsewhere)
        text_widget.tag_configure("highlight", background="#C9E2FF")  # Pale blue color
