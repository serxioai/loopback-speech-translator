#translation_view.py

import tkinter as tk
from tkinter import font as tkfont
import time

class TranslationView(tk.Frame):
    def __init__(self, session, root, 
                 on_start_speech_session_callback,
                 on_stop_speech_session_callback,
                 on_change_recognizing_event_rate_callback, 
                 ):
        super().__init__(root)
        self.session = session
        self.root = root
        self.on_change_recognizing_event_rate_callback = on_change_recognizing_event_rate_callback
        self.on_start_speech_session_callback = on_start_speech_session_callback
        self.on_stop_speech_session_callback = on_stop_speech_session_callback
        self.pack(expand=True, fill=tk.BOTH)
        self.launch()
        
    def launch(self):

        self.session.set_recognizing_callback(self.on_recognizing_updated)
        self.session.set_recognized_callback(self.on_recognized_updated)

        # Define the font
        font = tkfont.Font(family="Helvetica", size=15)

        # Create a frame
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Configure the grid weights for the frame
        self.frame.grid_rowconfigure(0, weight=1)  # Top row
        self.frame.grid_rowconfigure(1, weight=1)  # Bottom row
        self.frame.grid_columnconfigure(0, weight=1)  # Left column
        self.frame.grid_columnconfigure(1, weight=1)  # Right column

        # Setup the viewing windows for recognized and recognizing events
        self.recognizing_text_source = tk.Text(self.frame, bg="white", font=font, height=1)
        self.recognized_text_source = tk.Text(self.frame, bg="white", font=font, height=5)
        
        self.recognizing_text_target = tk.Text(self.frame, bg="white", font=font, height=1)
        self.recognized_text_target = tk.Text(self.frame, bg="white", font=font, height=5)

        # Place the cells on the grid with padding
        padding = 1  # You can adjust this value as needed
        self.recognizing_text_source.grid(row=0, column=0, sticky="nsew", padx=padding, pady=padding)
        self.recognizing_text_target.grid(row=0, column=1, sticky="nsew", padx=padding, pady=padding)
        self.recognized_text_source.grid(row=1, column=0, sticky="nsew", padx=padding, pady=padding)
        self.recognized_text_target.grid(row=1, column=1, sticky="nsew", padx=padding, pady=padding)

        # Add a bar at the bottom
        self.bottom_bar = tk.Frame(self)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Add "Start" and "Stop" buttons to the bottom bar
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.on_start_speech_session_callback)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.on_stop_speech_session_callback)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

        # The slider to modify the recognizing event rate
        self.recognizing_rate_slider = tk.Scale(self.bottom_bar, from_=0, to=8, orient='horizontal', label='Recognizing Event Rate')
        self.recognizing_rate_slider.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.recognizing_rate_slider.set(0)  # Default position at the middle of the scale
        self.recognizing_rate_slider.bind("<Motion>", lambda event: self.on_change_recognizing_event_rate_callback(self.recognizing_rate_slider.get()))

    def start_session(self):
         pass
    
    def stop_session(self):
         pass
        
    def clear_screen(self):
        self.recognizing_text_source.delete(1.0, tk.END)
        self.recognizing_text_target.delete(1.0, tk.END)
        self.recognized_text_source.delete(1.0, tk.END)
        self.recognized_text_target.delete(1.0, tk.END)

    def update_recognized_texts(self, recognized_source, recognized_target):
        current_time = time.strftime("%H:%M:%S")  # Get current time
        timestamped_source = f"{current_time} - {recognized_source}"
        timestamped_target = f"{current_time} - {recognized_target}"

        # Insert the timestamped texts at the beginning of the text widget
        self.recognized_text_source.insert("1.0", timestamped_source + "\n\n")
        self.recognized_text_target.insert("1.0", timestamped_target + "\n\n")

        # Highlight the newly inserted text
        self.highlight_text(self.recognized_text_source)
        self.highlight_text(self.recognized_text_target)

    # Update the screen with the contents of the observable buffer
    def update_recognizing_texts(self, recognizing_source, recognizing_target):
        self.recognizing_text_source.delete(1.0, tk.END)
        self.recognizing_text_source.insert(tk.END, recognizing_source + "\n\n")
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
                recognized_text_source = self.session.get_recognized_translations(lang)
            if index == 1:
                recognized_text_target = self.session.get_recognized_translations(lang)

        # Update the UI with translations
        self.update_recognized_texts(recognized_text_source, recognized_text_target)

    def on_recognizing_updated(self):
        # Iterate through each language code in the list
        for index, language_code in enumerate(self.session.target_languages):
            # Call display_text with the current language code
            if index == 0:
                self.display_recognizing_text(language_code, self.recognizing_text_source)
            if index == 1:
                self.display_recognizing_text(language_code, self.recognizing_text_target)

    def display_recognizing_text(self, language, text_widget):
        # Clear the text widget
        text_widget.delete(1.0, tk.END)

        # Fetch translations for the given language
        translations = self.session.get_next_transcription(language)
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
