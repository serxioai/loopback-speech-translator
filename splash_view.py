import tkinter as tk
from PIL import Image, ImageTk

class SplashView(tk.Frame):
    def __init__(self, parent, image_path, duration=3000, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.duration = duration
        self.callback = callback

        # Load and display the image
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo)
        label.image = photo  # Keep a reference
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Center the splash screen
        self.pack(expand=True, fill=tk.BOTH)

        # Schedule the splash screen to close
        self.after(self.duration, self.on_close)

    def on_close(self):
        if self.callback:
            self.callback()
        self.destroy()