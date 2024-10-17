import tkinter as tk
from tkinter import font as tkfont

class SignUpView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sign Up")
        self.geometry("350x437")
        self.configure(bg="white")

        # Placeholder for the logo
        self.logo_label = tk.Label(self, text="Logo", bg="white", font=tkfont.Font(size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 10))

        # Sign up label
        self.sign_up_label = tk.Label(self, text="Sign up", bg="white", font=tkfont.Font(size=16))
        self.sign_up_label.pack()

        # Already have an account
        self.login_label = tk.Label(self, text="Already have an account? Log in", bg="white", fg="blue", cursor="hand2", font=tkfont.Font(size=10))
        self.login_label.pack(pady=(5, 20))

        # Email entry
        self.email_label = tk.Label(self, text="Email", bg="white", font=tkfont.Font(size=12))
        self.email_label.pack(anchor="w", padx=20)
        self.email_entry = tk.Entry(self, font=tkfont.Font(size=12))
        self.email_entry.pack(fill="x", padx=20, pady=(0, 20))

        # Continue button
        self.continue_button = tk.Button(self, text="Continue", bg="#1E3A8A", fg="white", font=tkfont.Font(size=12), height=2)
        self.continue_button.pack(fill="x", padx=20)

        # Privacy policy
        self.privacy_label = tk.Label(self, text="Kasana uses cookies. For further details, please read our Privacy Policy.", bg="white", font=tkfont.Font(size=8), wraplength=300)
        self.privacy_label.pack(pady=(20, 10))

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy, font=tkfont.Font(size=12))
        self.close_button.pack(pady=(0, 20))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = SignUpView(master=root)
    app.mainloop()
