import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, parent, login_callback, register_callback):
        super().__init__(parent)
        self.login_callback = login_callback
        self.register_callback = register_callback
        self.build_ui()

    def build_ui(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.on_login_pressed)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="Register", command=self.on_register_pressed)
        self.register_button.pack()

    def on_login_pressed(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_callback(username, password)

    def on_register_pressed(self):
        self.register_callback()

    def display_error(self, message):
        messagebox.showerror("Error", message)
