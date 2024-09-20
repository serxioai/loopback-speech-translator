import tkinter as tk
from tkinter import ttk

class LoginView(tk.Toplevel):
    def __init__(self, master, login_callback, register_callback):
        super().__init__(master)
        self.login_callback = login_callback
        self.register_callback = register_callback
        
        self.geometry("400x500")
        self.configure(bg="white")
        self.transient(master)
        self.grab_set()
        
        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Log in to Kasana", font=("Arial", 20, "bold")).pack(pady=(0, 20))

        ttk.Label(main_frame, text="Email").pack(anchor="w")
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(main_frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, show="*", width=40)
        self.password_entry.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(main_frame, text="Forgot your password?", foreground="#0000FF", cursor="hand2").pack(anchor="w", pady=(0, 20))

        login_button = ttk.Button(main_frame, text="Log in", command=self.on_login_pressed, style="AccentButton.TButton")
        login_button.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(main_frame, text="OR").pack()

        sso_button = ttk.Button(main_frame, text="Log in with SSO", command=self.on_sso_pressed)
        sso_button.pack(fill=tk.X, pady=(20, 30))

        ttk.Label(main_frame, text="Sign up to make the most of Kasana:", font=("Arial", 12, "bold")).pack()
        ttk.Label(main_frame, text="Get a free account", foreground="#0000FF", cursor="hand2").pack()
        ttk.Label(main_frame, text="Try Kasana Pro for free", foreground="#0000FF", cursor="hand2").pack()

        self.style = ttk.Style()
        self.style.configure("AccentButton.TButton", background="#1a2b3c", foreground="white")

    def on_login_pressed(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.login_callback(email, password)

    def on_sso_pressed(self):
        # Implement SSO login logic here
        pass

    def on_register_pressed(self):
        self.register_callback()
