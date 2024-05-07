import tkinter as tk

class TranslationView(tk.Frame):
        
    def build_view(self):
            
            # Define the font
            font = tkfont.Font(family="Helvetica", size=12)

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

            # The slider to modify the recognizing event rate
            self.recognizing_rate_slider = tk.Scale(self.bottom_bar, from_=0, to=8, orient='horizontal', label='Recognizing Event Rate')
            self.recognizing_rate_slider.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
            self.recognizing_rate_slider.set(0)  # Default position at the middle of the scale
            self.recognizing_rate_slider.bind("<Motion>", lambda event: self.speechAPI.set_recognizing_event_rate(self.recognizing_rate_slider.get()))

    def start_session(self):
         pass
    
    def stop_session(self):
         pass
        
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
        recognized_text_source = self.speechAPI.get_recognized_translations("en")
        recognized_text_target = self.speechAPI.get_recognized_translations("es")

        # Update the UI with translations
        self.update_recognized_texts(recognized_text_source, recognized_text_target)

    def on_recognizing_updated(self):
        self.display_source_text(source_language)
        self.display_target_text(target_language)

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
