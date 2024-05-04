def animate_ellipses():
    if self.is_recognizing:
        current_text = self.label_status.cget("text")
        if current_text.endswith("..."):
            new_text = current_text[:-3]  # Remove ellipses
        else:
            new_text = current_text + "."  # Add an ellipsis

        self.label_status.config(text=new_text)
        self.after(500, self.animate_ellipses)  # Recursive call after 500ms


    def on_session_started(self):
        animate_ellipses()