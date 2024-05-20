# new_session_view.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ConfigSessionView(tk.Toplevel):
    def __init__(self, parent, on_start_session):
        self.on_start_session = on_start_session # Connect to the controller
        super().__init__(parent)
        self.title("Configure Speech Session")
        self.geometry("300x300")
        self.transient(parent)
        self.session_config_data = {}

        self.grab_set()
        self.build_ui()

    def build_ui(self):
        # Create a variable to store the selection
        self.audio_source_option = tk.StringVar(value="default")
        self.source_language_option = tk.StringVar()
        self.target_language_option = tk.StringVar()

        # Create radio buttons
        self.radio_headphones = ttk.Radiobutton(self, text="Headphones", value="headphones",
                                                variable=self.audio_source_option)
        self.radio_default_mic = ttk.Radiobutton(self, text="Default Mic", value="default",
                                                variable=self.audio_source_option)
        self.radio_headphones.pack()
        self.radio_default_mic.pack()

        # Language options for the dropdown menus
        self.language_options = ['English', 'Spanish', 'French', 'German']

        # Create and setup comboboxes for source and target languages
        ttk.Label(self, text="Source Language:").pack()
        self.combobox1 = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.source_language_option)
        self.combobox1.set('Select Source Language')
        self.combobox1.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self, text="Target Language:").pack()
        self.combobox2 = ttk.Combobox(self, values=self.language_options, state='readonly', textvariable=self.target_language_option)
        self.combobox2.set('Select Target Language')
        self.combobox2.pack(fill=tk.X, padx=5, pady=5)

        # OK button to submit the selections
        ttk.Button(self, text="OK", command=self.submit).pack(pady=10)

    def submit(self):
        source_lang = self.source_language_option.get()
        target_lang = self.target_language_option.get()

        if source_lang == target_lang:
            messagebox.showerror("Language Selection Error", "Source and target languages must be different.")
            return

        # Check if both languages are valid options
        if source_lang not in self.language_options or target_lang not in self.language_options:
            messagebox.showerror("Language Selection Error", "Please select valid languages from the list.")
            return  # Stop processing and allow user to correct the input
        
        self.process_and_close(source_lang, target_lang)

    def process_and_close(self, source_lang, target_lang):

        audio_source = self.audio_source_option.get()

        language_options = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de'
        }

        # Build the speech session dict
        self.session_config_data = {
            'audio_source': audio_source,
            'speech_rec_lang':'en-US',
            'detectable_lang':["en-US", "es-MX"],
            'languages': {
                'input': language_options[source_lang],
                'output': language_options[target_lang]
            }
        }

        try:
            self.on_start_session(self.session_config_data)
            print("Callback executed successfully.")
        except Exception as e:
            print("Error in executing callback:", e)
        finally:
            self.destroy()
    

