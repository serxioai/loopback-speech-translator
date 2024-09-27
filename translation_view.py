# translation_view.py

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from login_view import LoginView
from tkinter import messagebox
from event_signal_buffer import EventSignalBuffer, Observer

# TODO: move this to a config file
language_options = {
    'English (American)': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de'
}

detectable_languages = ["en-US", "es-MX"]
speech_recognition_language = "en-US"

class TranslationView(tk.Frame, Observer):
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

        self.event_signal_buffer = azure_speech_translate_api.get_event_signal_buffer()
        self.event_signal_buffer.attach(self)
        
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

        # Translation display windows
        self.source_language_text = tk.Text(self, bg="white", font=display_font, wrap="word")
        self.target_language_text = tk.Text(self, bg="white", font=display_font, wrap="word")

        # Place the text widgets in the frames
        self.source_language_text.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        self.target_language_text.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)

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
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.start_streaming)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.stop_streaming)
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

    # text_widget.see(tk.END) for continuous scrolling

    def update_display(self, data, reason):
        for lang, translations in data.items():
            # Determine which text widget to use
            if lang == language_options[self.source_language_option.get()]:
                text_widget = self.source_language_text
            elif lang == language_options[self.target_language_option.get()]:
                text_widget = self.target_language_text
            else:
                continue  # Skip if the language doesn't match source or target

            if reason == "RECOGNIZING":
                # Get the current content of the first line (this includes previously concatenated text)
                current_text = text_widget.get("1.0", tk.END).strip()

                # Initialize processed_text and highlight indices
                processed_text = ""
                highlight_indices = []
                current_position = len(current_text)  # Start position for new text is at the end of current content

                # Process each string in the list
                for translation in translations:
                    i = 0
                    while i < len(translation):
                        if translation[i] == '+' and i < len(translation) - 1:
                            processed_text += translation[i + 1]  # Add the character after the '+'
                            highlight_indices.append(current_position)  # Track position for highlighting
                            current_position += 1
                            i += 2  # Skip the '+' and the next character
                        else:
                            processed_text += translation[i]
                            current_position += 1
                            i += 1

                # Append the new RECOGNIZING text to the current content without re-adding the previous text
                final_recognizing_text = current_text + " " + processed_text if current_text else processed_text

                # Update the first line of the text widget with the new content
                text_widget.delete("1.0", "2.0")  # Clear the first line where RECOGNIZING text is displayed
                text_widget.insert("1.0", final_recognizing_text + '\n')  # Insert the new concatenated sentence

                # Apply highlighting to the newly added content
                for index in highlight_indices:
                    text_widget.tag_add("highlight", f"1.{index}", f"1.{index + 1}")

                # Configure the highlight style (blue background for the highlighted letters)
                text_widget.tag_configure("highlight", background="#C9E2FF")

            elif reason == "RECOGNIZED":
                # Process recognized text similarly to remove '+' signs
                processed_text = ""
                i = 0
                for translation in translations:
                    while i < len(translation):
                        if translation[i] == '+' and i < len(translation) - 1:
                            processed_text += translation[i + 1]  # Add the character after the '+'
                            i += 2  # Skip the '+' and the next character
                        else:
                            processed_text += translation[i]
                            i += 1

                # Insert RECOGNIZED text below the RECOGNIZING content (at the end of the widget)
                text_widget.insert(tk.END, processed_text + '\n')

            # Ensure the widget updates immediately
            text_widget.update_idletasks()

            


    def clear_screen(self): 
        self.translated_languages.delete(1.0, tk.END)
        self.detected_languages_text.delete(1.0, tk.END)
    
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

       
