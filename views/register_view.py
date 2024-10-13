import tkinter as tk
from tkinter import messagebox

class RegisterView(tk.Toplevel):
    def __init__(self, parent, create_account_callback):
        super().__init__(parent)
        self.create_account_callback = create_account_callback
        self.build_ui()

    def build_ui(self):
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.create_account_button = tk.Button(self, text="Create Account", command=self.on_create_account_pressed)
        self.create_account_button.pack()

    def on_create_account_pressed(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.create_account_callback(email, username, password)

    def display_error(self, message):
        messagebox.showerror("Error", message)
