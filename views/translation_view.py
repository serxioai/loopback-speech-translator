# translation_view.py

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from views.login_view import LoginView
from tkinter import messagebox
from recognizing_event_signal_buffer import RecognizingBufferObserver
from recognized_event_signal_buffer import RecognizedBufferObserver
from user_settings import UserSettings
from languages import Languages
import configparser


class TranslationView(tk.Frame, RecognizingBufferObserver, RecognizedBufferObserver):
    def __init__(self, 
                 root, 
                 azure_speech_translate_api,
                 user_settings):
        super().__init__(root)
        self.root = root    
        self.azure_speech_translate_api = azure_speech_translate_api
        self.user_settings = user_settings
        
        # Initialize config
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        # Initialize languages and language_options
        self.languages = Languages()
        self.language_options = self.languages.get_language_options()  

        # Watch the event signal buffers for changes
        self.recognizing_event_buffer = azure_speech_translate_api.get_recognizing_event_buffer()
        self.recognizing_event_buffer.attach(self)
        self.recognized_event_buffer = azure_speech_translate_api.get_recognized_event_buffer()
        self.recognized_event_buffer.attach(self)
        
        # Ensure the frame expands
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.build_ui()
       
    def build_ui(self):
        
        self.source_language_option = tk.StringVar()
        self.target_language_option = tk.StringVar()
    
        # Define gui fonts and styles
        display_font = tkfont.Font(family="Arial Unicode MS", size=25)

        self.grid_columnconfigure(0, weight=2)  # Left column
        self.grid_columnconfigure(1, weight=2)  # Right column
        self.grid_rowconfigure(0, weight=0)  # Top row for dropdowns
        self.grid_rowconfigure(1, weight=1)  # Middle row for text
        self.grid_rowconfigure(2, weight=1)  # Middle row for text
        self.grid_rowconfigure(3, weight=0)  # Bottom row for buttons

        # Left dropdown (source language)
        self.source_language_dropdown = ttk.Combobox(self, state='readonly', textvariable=self.source_language_option)
        self.source_language_dropdown['values'] = [lang['name'] for lang in self.language_options['languages']]
        self.source_language_dropdown.set(self.user_settings.get_default_source_language())
        self.source_language_dropdown.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.source_language_dropdown.bind("<<ComboboxSelected>>", self.update_default_source_language)
        
        # Right dropdown (target language)
        self.target_language_dropdown = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.target_language_option)
        self.target_language_dropdown['values'] = [lang['name'] for lang in self.language_options['languages']]
        self.target_language_dropdown.set(self.user_settings.get_default_target_language())
        self.target_language_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.target_language_dropdown.bind("<<ComboboxSelected>>", self.update_default_target_language)

        # Translation display windows for history and realtime
        self.source_language_text_history = tk.Text(self, bg="white", font=display_font, wrap="word")
        self.target_language_text_history = tk.Text(self, bg="white", font=display_font, wrap="word")

        self.source_language_realtime_text = tk.Text(self, bg="white", font=display_font, wrap="word")
        self.target_language_realtime_text = tk.Text(self, bg="white", font=display_font, wrap="word")

        # Place the text widgets in the frames
        self.source_language_realtime_text.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        self.target_language_realtime_text.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)

        self.source_language_text_history.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
        self.target_language_text_history.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)

        # Add scrolling to the text widgets
        self.source_language_text_history.see(tk.END)
        self.target_language_text_history.see(tk.END)
        self.source_language_realtime_text.see(tk.END)
        self.target_language_realtime_text.see(tk.END)

        # Add a bar at the bottom
        self.bottom_bar = tk.Frame(self)
        self.bottom_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Configure grid columns for spacing
        self.bottom_bar.grid_columnconfigure(0, weight=1)
        self.bottom_bar.grid_columnconfigure(1, weight=1)

        # Add "Start" and "Stop" buttons to the bottom bar
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.start_streaming, height=2)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.stop_streaming, height=2)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def update_recognizing_event_display(self, output_dict):
        for lang, translations in output_dict.items():
            source_lang_code = self.languages.get_language_code_from_name(self.source_language_option.get())
            target_lang_code = self.languages.get_language_code_from_name(self.target_language_option.get())
            # Determine which text widget to use
            if lang == source_lang_code:
                text_widget = self.source_language_realtime_text
            elif lang == target_lang_code:
                text_widget = self.target_language_realtime_text
            else:
                continue  # Skip if the language doesn't match source or target
            
            # Clear the text widget
            text_widget.delete(1.0, tk.END)
            
            # Configure highlighting tag before processing the translation
            text_widget.tag_configure("highlight", background="#C9E2FF")  # Pale blue color

            # Iterate through the translation string
            i = 0
            while i < len(translations):
                if translations[i] == '+' and i < len(translations) - 1:
                    # Insert the next character after '+'
                    char_to_insert = translations[i + 1]
                    text_widget.insert(tk.END, char_to_insert)

                    # Get the current position for the just-inserted character
                    start_index = f"{text_widget.index(tk.END)} - 2c"
                    end_index = text_widget.index(tk.END)

                    # Highlight the character
                    text_widget.tag_add("highlight", start_index, end_index)

                    i += 2  # Move past the '+' and the next character
                else:
                    # Insert other characters normally
                    text_widget.insert(tk.END, translations[i])
                    i += 1

    def update_recognized_event_display(self, translations):
        for lang, translation in translations.items():
            source_lang_code = self.languages.get_language_code_from_name(self.source_language_option.get())
            target_lang_code = self.languages.get_language_code_from_name(self.target_language_option.get())        
            # Determine which text widget to use
            if lang == source_lang_code:
                text_widget = self.source_language_text_history
            elif lang == target_lang_code:
                text_widget = self.target_language_text_history

            # Clear the text widget
            text_widget.delete(1.0, tk.END)

            if isinstance(translation, list):
                translation = '\n'.join(translation)

            # Insert the translation into the text widget with alternating background colors
            lines = translation.split('\n')
            for i, line in enumerate(lines):
                if i % 2 == 0:
                    text_widget.insert("1.0", f"{line}\n", ("gray_bg",))
                else:
                    text_widget.insert("1.0", f"{line}\n")

            # Configure the tag for gray background
            text_widget.tag_configure("gray_bg", background="#e6e6e6")
    
    def start_streaming(self):
        # Get the source and target languages from the dropdowns
        source_lang = self.source_language_option.get()
        target_lang = self.target_language_option.get()

        # Validate the language selection
        translated_languages = self.validate_language_selection(source_lang, target_lang)

        if translated_languages:
            session_data = self.get_session_data(translated_languages)
            self.azure_speech_translate_api.start_streaming(session_data)

    def stop_streaming(self):
        self.azure_speech_translate_api.stop_streaming()
    
    def get_session_data(self, translated_languages):
        session_data = {
                'audio_source': self.user_settings.get_audio_source(),
                'speech_rec_lang': self.user_settings.get_default_speech_recognition_language(),
                'detectable_lang': self.user_settings.get_default_detectable_languages(),
                'session_languages': translated_languages
            }
        return session_data

    def validate_language_selection(self, source_lang, target_lang):

        source_lang_code = self.languages.get_language_code_from_name(source_lang)
        target_lang_code = self.languages.get_language_code_from_name(target_lang)

        if source_lang_code == target_lang_code:
            messagebox.showerror("Language Selection Error", "Source and target languages must be different.")
            return False

        session_languages = [source_lang_code,target_lang_code]

        return session_languages

    def update_default_source_language(self, event=None):
        new_language = self.source_language_option.get()
        self.user_settings.set_default_source_language(new_language) # This is the language code without the locale, i.e. es
        self.update_default_detectable_languages(new_language, self.target_language_option.get())

    def update_default_target_language(self, event=None):
        new_language = self.target_language_option.get()
        self.user_settings.set_default_target_language(new_language)
        self.update_default_detectable_languages(self.source_language_option.get(), new_language)

    def update_default_detectable_languages(self, source_language, target_language, event=None):
        source_language_code = self.languages.get_language_locale_from_name(source_language)  
        target_language_code = self.languages.get_language_locale_from_name(target_language)
        languages = [source_language_code, target_language_code]
        self.user_settings.set_default_detectable_languages(languages)
