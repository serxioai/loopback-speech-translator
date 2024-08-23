# translation_view.py

import tkinter as tk
from tkinter import font as tkfont
import time
from tkinter.font import Font

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
        #self.current_session.set_recognized_callback(self.on_recognized_updated)
       
    def build_ui(self):
        
        # Define gui fonts and styles
        display_font = tkfont.Font(family="Arial Unicode MS", size=25)

        self.grid_columnconfigure(0, weight=2)  # Left column (3/5)
        self.grid_columnconfigure(1, weight=2)  # Right column (3/5)
        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=0)  # Bottom row

        # Text display windows
        self.translated_languages = tk.Text(self, bg="white", font=display_font)  # RECOGNIZING status
        self.detected_languages_text = tk.Text(self, bg="white", font=display_font)

        # Place the text widgets in the frames
        self.detected_languages_text.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.translated_languages.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)

        # Add a bar at the bottom
        self.bottom_bar = tk.Frame(self)
        self.bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Configure grid columns for spacing
        self.bottom_bar.grid_columnconfigure(0, weight=1)
        self.bottom_bar.grid_columnconfigure(1, weight=1)
        self.bottom_bar.grid_columnconfigure(2, weight=1)
        self.bottom_bar.grid_columnconfigure(3, weight=1)
        self.bottom_bar.grid_columnconfigure(4, weight=1)

        # Add "Start" and "Stop" buttons to the bottom bar
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.on_start_speech_session_callback)
        self.start_button.grid(row=0, column=1, padx=10, pady=5)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.on_stop_speech_session_callback)
        self.stop_button.grid(row=0, column=2, padx=10, pady=5)

        # Add a slider vertically to the right of the buttons
        self.recognizing_rate_slider = tk.Scale(self.bottom_bar, from_=0, to=5, orient='horizontal', label='')
        self.recognizing_rate_slider.grid(row=0, column=3, padx=10, pady=5)
        self.recognizing_rate_slider.set(0)
        self.recognizing_rate_slider.bind("<Motion>", lambda event: self.on_change_recognizing_event_rate_callback(self.recognizing_rate_slider.get()))

   
    def clear_screen(self):
        self.translated_languages.delete(1.0, tk.END)
        self.detected_languages_text.delete(1.0, tk.END)

    def update_text_widget(self, text):
        print("Updating text widget...")
        self.detected_languages_text.delete('1.0', 'end')  # Clear existing text
        self.detected_languages_text.insert('end', text)  # Insert new text
        print("Update complete.")

    def insert_at_top(text_widget, text, tag=None):
        # Insert new text at 'top_insert' mark position
        text_widget.insert('top_insert', text + "\n", tag)
        # Move the 'top_insert' mark to just after the newly inserted text
        text_widget.mark_set("top_insert", "top_insert + 1 line")
    
    def display_recognized_translations(self, current_time, input_transcription, output_translation):
        arrow_shape = '↳'
        arrow_font = Font(family="Arial Unicode MS", size=30)

        self.detected_languages_text.insert('1.0', f"{output_translation}\n", 'display_font')
        self.detected_languages_text.tag_config('arrow_font', font=arrow_font, foreground="#0EA1EA")
        self.detected_languages_text.insert('1.0', f"\t{arrow_shape}", 'arrow_font')  # Unicode character U+21B3
        self.detected_languages_text.insert('1.0', f"{input_transcription}\n", 'display_font')
        self.detected_languages_text.insert('1.0', f"\n{current_time}:\n\n", 'bold_font')

    # def on_recognized_updated(self):
    #     arrow_shape = '↳'
    #     arrow_font = Font(family="Arial Unicode MS", size=30)

    #     # time_stamp_font = Font(family="Arial Unicode MS", size=15)
    #     try:
    #         print("Updating recognized translations...")
    #         current_time = time.strftime("%H:%M:%S")  # Get current time
    #         print(f"Current Time: {current_time}")

    #         # Extract the input and output languages
    #         input_lang = self.current_session.languages['input']
    #         output_lang = self.current_session.languages['output']

    #         input_translation = self.current_session.get_recognized_translations(input_lang)
    #         output_translation = self.current_session.get_recognized_translations(output_lang)

    #         self.detected_languages_text.insert('1.0', f"{output_translation}\n", 'display_font')
    #         self.detected_languages_text.tag_config('arrow_font', font=arrow_font, foreground="#0EA1EA")
    #         self.detected_languages_text.insert('1.0', f"\t{arrow_shape}", 'arrow_font')  # Unicode character U+21B3
    #         self.detected_languages_text.insert('1.0', f"{input_translation}\n", 'display_font')
    #         self.detected_languages_text.insert('1.0', f"\n{current_time}:\n\n", 'bold_font')

    #     except Exception as e:
    #         print(f"Error during update: {e}")

    def on_recognizing_updated(self):
        self.display_recognizing_text(self.current_session.languages['output'], self.translated_languages)

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
