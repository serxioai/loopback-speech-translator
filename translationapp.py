import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv
from speech_api import SpeechAPI
import time
from modal_dialog import ModalDialog
import utils

# Load the .env file
load_dotenv()

subscriptionKey = os.environ.get("SPEECH_KEY")
serviceRegion = os.environ.get("SPEECH_REGION")

translationLanguages = ["es","en"]
source_language = "en"
target_language = "es"
speechRecognitionLanguage = "en-US"
detectableLanguages = ["en-US","es-MX"]
font = ("Arial", 22)
endSilenceTimeout = -1

class TranslationApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.speechAPI = None
        self.selected_audio_source = None
        self.build_frame()
        modal = ModalDialog(self)
        self.wait_window(modal)  # Wait for the modal dialog to close
         
    def start_session(self):
        # Start speech recognition or any other action you want
        print("Starting session...")
        self.clear_screen()

        # Set up the connection to Azure Speech
        self.speechAPI = SpeechAPI(subscription_key=subscriptionKey, 
                                   service_region=serviceRegion, 
                                   translation_languages=translationLanguages, 
                                   speech_recognition_language=speechRecognitionLanguage, 
                                   detectable_languages=detectableLanguages,
                                   selected_audio_source=self.selected_audio_source)
        
        # Connect the buffers holding the event results
        self.speechAPI.set_recognized_callback(self.on_recognized_updated)
        self.speechAPI.set_recognizing_callback(self.on_recognizing_updated)
        self.speechAPI.set_session_started_callback(self.on_session_started)
        self.speechAPI.configure_session()
        self.speechAPI.translation_recognizer.start_continuous_recognition()

    def clear_screen(self):
        self.recognizing_text_source.delete(1.0, tk.END)
        self.recognizing_text_target.delete(1.0, tk.END)
        self.recognized_text_source.delete(1.0, tk.END)
        self.recognized_text_target.delete(1.0, tk.END)

    def stop_session(self):
        # Stop speech recognition or any other action you want
        print("Stopping session...")
        self.speechAPI.translation_recognizer.stop_continuous_recognition()
        self.speechAPI.reset_translation_recognizer()

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

    def update_recognizing_texts(self, recognizing_source, recognizing_target): 
        self.recognizing_text_source.delete(1.0, tk.END)
        self.recognizing_text_source.insert(tk.END, recognizing_source + "\n\n")
        self.recognizing_text_target.delete(1.0,tk.END)
        self.recognizing_text_target.insert(tk.END, recognizing_target + "\n\n")

    # Callback method for the observer
    def on_recognized_updated(self):
        recognized_text_source = self.speechAPI.get_recognized_translations("en")
        recognized_text_target = self.speechAPI.get_recognized_translations("es")

        # Update the UI with translations
        self.update_recognized_texts(recognized_text_source, recognized_text_target)

    def on_session_started(self):
        utils.animate_ellipses()

    def on_recognizing_updated(self):
        recognizing_text_source = self.display_source_text(source_language)
        recognizing_text_target = self.display_target_text(target_language)

    def display_source_text(self, source_language):
        # Clear the text widget
        self.recognizing_text_source.delete(1.0, tk.END)

        translations = self.speechAPI.get_next_transcription(source_language)
        i = 0
        while i < len(translations):
            if translations[i] == '+' and i < len(translations) - 1: 
                self.recognizing_text_source.insert(tk.END, translations[i + 1])
                # Highlight the char
                self.recognizing_text_source.tag_add("highlight", f"{tk.END} - 2c", tk.END)
                i += 2  # Skip the next char, as we've already added it
            else:
                self.recognizing_text_source.insert(tk.END, translations[i])
                i += 1
    
    def display_target_text(self, target_language):
         # Clear the text widget
        self.recognizing_text_target.delete(1.0, tk.END)

        translations = self.speechAPI.get_next_transcription(target_language)
        i = 0
        while i < len(translations):
            if translations[i] == '+' and i < len(translations) - 1: 
                self.recognizing_text_target.insert(tk.END, translations[i + 1])
                # Highlight the char
                self.recognizing_text_target.tag_add("highlight", f"{tk.END} - 2c", tk.END)
                i += 2  # Skip the next char, as we've already added it
            else:
                self.recognizing_text_target.insert(tk.END, translations[i])
                i += 1

    def on_recognized_slider_change(self, value):
        self.speechAPI.set_end_silence_timeout(value)

    def trigger_recognized_event(self):
        self.speechAPI.trigger_recognized_event()

    def build_frame(self):
        # Create a frame
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)

         # Configure the grid weights for the frame
        self.frame.grid_rowconfigure(0, weight=1)  # Top row
        self.frame.grid_rowconfigure(1, weight=5)  # Bottom row
        self.frame.grid_columnconfigure(0, weight=1)  # Left column
        self.frame.grid_columnconfigure(1, weight=1)  # Right column

        # Setup the viewing windows for recognized and recognizing events
        self.recognizing_text_source = tk.Text(self.frame, bg="white", font=font, height=1)
        self.recognized_text_source = tk.Text(self.frame, bg="white", font=font, height=5)
        
        self.recognizing_text_target = tk.Text(self.frame, bg="white", font=font, height=1)
        self.recognized_text_target = tk.Text(self.frame, bg="white", font=font, height=5)

        self.recognizing_text_source = tk.Text(self.frame, bg="white", font=font, height=1)    
        self.recognized_text_source = tk.Text(self.frame, bg="white", font=font, height=5)
        
        self.recognizing_text_target = tk.Text(self.frame, bg="white",font=font, height=1)
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
        self.start_button = tk.Button(self.bottom_bar, text='Start', command=self.start_session)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

        self.stop_button = tk.Button(self.bottom_bar, text='Stop', command=self.stop_session)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800") 
    root.title("Loopback Speech Translator")
    app = TranslationApp(root)
    app.pack(expand=True, fill=tk.BOTH)  # Pack the app within the root window
    root.mainloop()
