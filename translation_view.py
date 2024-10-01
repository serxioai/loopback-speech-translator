# translation_view.py
import configparser

# Read settings from the settings.ini file
config = configparser.ConfigParser()
config.read('settings.ini')

# Extract settings
speech_detection_language = config.get('Settings', 'speech_detection_language', fallback='en-US')
audio_source = config.get('Settings', 'audio_source', fallback='blackhole')
logged_in_status = config.getboolean('Settings', 'logged_in_status', fallback=True)
default_source_language = config.get('Settings', 'default_source_language', fallback='Spanish (Mexico)')

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from login_view import LoginView
from tkinter import messagebox
from recognizing_event_signal_buffer import RecognizingBufferObserver
from recognized_event_signal_buffer import RecognizedBufferObserver

# TODO: move this to a config file
language_options = {
    'English (American)': 'en',
    'Spanish (Mexico)': 'es',
    'French': 'fr',
    'German': 'de'
}

detectable_languages = ["en-US", "es-MX"]
speech_recognition_language = "en-US"

class TranslationView(tk.Frame, RecognizingBufferObserver, RecognizedBufferObserver):
    def __init__(self, 
                 root, 
                 logged_in_status,
                 azure_speech_translate_api,
                 settings):
        super().__init__(root)
        self.root = root    
        self.logged_in_status = logged_in_status
        self.azure_speech_translate_api = azure_speech_translate_api
        self.settings = settings

        # Watch the buffers for changes
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

        # Language options
        self.language_options = ["English (American)", "Spanish (Mexico)", "French", "German"]

        # Left dropdown (source language)
        self.left_dropdown = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.source_language_option)
        self.left_dropdown.set(default_source_language)
        self.left_dropdown.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Right dropdown (target language)
        self.right_dropdown = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.target_language_option)
        self.right_dropdown.set("English (American)")
        self.right_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

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

    def update_recognizing_event_display(self, output_dict):
        for lang, translations in output_dict.items():
            source_lang_code = language_options.get(self.source_language_option.get())
            target_lang_code = language_options.get(self.target_language_option.get())
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
            # Determine which text widget to use
            if lang == language_options[self.source_language_option.get()]:
                text_widget = self.source_language_text_history
            elif lang == language_options[self.target_language_option.get()]:
                text_widget = self.target_language_text_history

            # Clear the text widget
            text_widget.delete(1.0, tk.END)

            if isinstance(translation, list):
                translation = '\n'.join(translation)

            # Insert the translation into the text widget with alternating background colors
            lines = translation.split('\n')
            for i, line in enumerate(lines):
                if i % 2 == 0:
                    text_widget.insert(tk.END, f"{line}\n", ("gray_bg",))
                else:
                    text_widget.insert(tk.END, f"{line}\n")

            # Configure the tag for gray background
            text_widget.tag_configure("gray_bg", background="#e6e6e6")
    
    def start_streaming(self):
        source_lang = self.source_language_option.get()
        target_lang = self.target_language_option.get()
        audio_source = self.settings["audio_source"]

        translated_languages = self.validate_language_selection(source_lang, target_lang)
        if translated_languages:
            # Build the speech session dict
            audio_source = self.settings["audio_source"]
            speech_recognition_language = self.settings["speech_detection_language"]

            session_data = {
                'audio_source': audio_source,
                'speech_rec_lang': speech_recognition_language,
                'detectable_lang': detectable_languages,
                'translated_languages': translated_languages
            }

            self.azure_speech_translate_api.start_streaming(session_data)

            return session_data

    def stop_streaming(self):
        self.azure_speech_translate_api.stop_streaming()

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

       
