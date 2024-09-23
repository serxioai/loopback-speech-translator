# translation_view.py

import tkinter as tk
from tkinter import font as tkfont
from tkinter.font import Font
from tkinter import ttk
from login_view import LoginView
from tkinter import messagebox
from azure_speech_translate_api import AzureSpeechTranslateAPI

# TODO: move this to a config file
language_options = {
    'English (American)': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de'
}

detectable_languages = ["en-US", "es-MX"]

speech_recognition_language = "en-US"

class TranslationView(tk.Frame):
    def __init__(self, 
                 root, 
                 logged_in_status,
                 on_start_speech_session_callback,
                 on_stop_speech_session_callback,
                 azure_speech_translate_api):
        super().__init__(root)
        self.root = root    
        self.logged_in_status = logged_in_status
        self.on_start_speech_session_callback = on_start_speech_session_callback
        self.on_stop_speech_session_callback = on_stop_speech_session_callback
        self.azure_speech_translate_api = azure_speech_translate_api
        self.grid(sticky="nsew")

        # Ensure the frame expands
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
 
        self.build_ui()

        self.azure_speech_translate_api.set_recognizing_callback(self.on_recognizing_updated)
        self.azure_speech_translate_api.set_recognized_callback(self.on_display_recognized_speech)
       
    def build_ui(self):
        
        self.source_language_option = tk.StringVar()
        self.target_language_option = tk.StringVar()
    
        # Define gui fonts and styles
        display_font = tkfont.Font(family="Arial Unicode MS", size=25)

        self.grid_columnconfigure(0, weight=2)  # Left column
        self.grid_columnconfigure(1, weight=2)  # Right column
        self.grid_rowconfigure(0, weight=0)  # Top row for dropdowns
        self.grid_rowconfigure(1, weight=1)  # Middle row for text
        self.grid_rowconfigure(2, weight=0)  # Bottom row for buttons

        # Language options
        self.language_options = ["English (American)", "Spanish", "French", "German"]

        # Left dropdown (source language)
        self.left_dropdown = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.source_language_option)
        self.left_dropdown.set("Select source language")
        self.left_dropdown.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Right dropdown (target language)
        self.right_dropdown = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.target_language_option)
        self.right_dropdown.set("English (American)")
        self.right_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Text display windows
        self.detected_languages_text = tk.Text(self, bg="white", font=display_font)
        self.translated_languages = tk.Text(self, bg="white", font=display_font)

        # Place the text widgets in the frames
        self.detected_languages_text.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        self.translated_languages.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)

        # Add a bar at the bottom
        self.bottom_bar = tk.Frame(self)
        self.bottom_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Configure grid columns for spacing
        self.bottom_bar.grid_columnconfigure(0, weight=1)
        self.bottom_bar.grid_columnconfigure(1, weight=1)
        self.bottom_bar.grid_columnconfigure(2, weight=1)
        self.bottom_bar.grid_columnconfigure(3, weight=1)
        self.bottom_bar.grid_columnconfigure(4, weight=1)

        # Add "Start" and "Stop" buttons to the bottom bar
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.submit)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.on_stop_stream_translation)
        self.stop_button.grid(row=0, column=1, padx=10, pady=5)

        if not self.logged_in_status:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.display_login_view()
    
    def display_login_view(self):
        # Create a Toplevel window
        self.login_window = tk.Toplevel(self.root)
        self.login_window.transient(self.root)  # Make the window modal
        self.login_window.grab_set()  # Ensure all events are directed to this window

        # Create the LoginView inside the Toplevel window
        self.login_view = LoginView(self.login_window, self.on_login, self.on_register)
        self.login_view.grid(row=0, column=0, sticky="nsew")

        # Center the modal window over the root window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (self.login_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (self.login_window.winfo_height() // 2)
        self.login_window.geometry(f"+{x}+{y}")

    def clear_screen(self): 
        self.translated_languages.delete(1.0, tk.END)
        self.detected_languages_text.delete(1.0, tk.END)
    
    def submit(self):
        source_lang = self.source_language_option.get()
        target_lang = self.target_language_option.get()
        audio_source = self.audio_source_option.get()

        translated_languages = self.validate_language_selection(source_lang, target_lang)
        if translated_languages:
            encoded_session_data = self.encode_session_data(translated_languages, audio_source)    
        
        self.on_stream_translation(encoded_session_data)

    def encode_session_data(self, translated_languages, audio_source):
         # Build the speech session dict
        session_data = {
            'audio_source': audio_source,
            'speech_rec_lang': speech_recognition_language,
            'detectable_lang': detectable_languages,
            'translated_languages': translated_languages
        }
        
        print("SESSION DATA: ", session_data)

        return session_data

    def validate_language_selection(self, source_lang, target_lang):
        if source_lang == target_lang:
            messagebox.showerror("Language Selection Error", "Source and target languages must be different.")
            return False

        if source_lang not in self.language_options or target_lang not in self.language_options:
            messagebox.showerror("Language Selection Error", "Please select valid languages from the list.")
            return False

        translated_languages = {
                'source': language_options[source_lang],
                'target': language_options[target_lang]
            }

        return translated_languages
    
    def on_stream_translation(self, encoded_session_data):
        self.azure_speech_translate_api.start_streaming(encoded_session_data)

    def on_stop_stream_translation(self):
        self.azure_speech_translate_api.stop_streaming()

    def on_display_recognized_speech(self, current_time, input_transcription, output_translation):
        arrow_shape = '↳'
        arrow_font = Font(family="Arial Unicode MS", size=30)

        self.detected_languages_text.insert('1.0', f"{input_transcription}\n", 'display_font')
        self.detected_languages_text.tag_config('arrow_font', font=arrow_font, foreground="#0EA1EA")
        self.detected_languages_text.insert('1.0', f"\t{arrow_shape}", 'arrow_font')  # Unicode character U+21B3
        self.detected_languages_text.insert('1.0', f"{output_translation}\n", 'display_font')
        self.detected_languages_text.insert('1.0', f"\n{current_time}:\n\n", 'bold_font')

    def on_recognizing_updated(self):
        self.display_recognizing_text(self.languages['output'], self.translated_languages)

    def display_recognizing_speech(self, language, text_widget):

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