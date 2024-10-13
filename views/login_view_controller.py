import tkinter as tk
from tkinter import messagebox
from login_view import LoginView
from auth_model import AuthModel
from views.register_view import RegisterView    

class LoginViewController:
    def __init__(self, root, user_settings, on_login_success):
        self.root = root
        self.user_settings = user_settings
        self.auth_model = AuthModel()
        self.login_view = None
        self.register_view = None
        self.on_login_success = on_login_success  # Callback for successful login
        self.menu_index_login = None

    def display_login_view(self):
        if self.login_view is None or not self.login_view.winfo_exists():
            # Create a new login view if it doesn't exist
            self.login_view = LoginView(self.root, self.login, self.register_callback)
        else:
            # If the login view already exists, bring it to the front
            self.login_view.deiconify()
            self.login_view.lift()
            self.login_view.focus_force()

    # Callback for the login button click
    def login(self, username, password):
        print("In the login view controller login method")
        user_doc = self.auth_model.authenticate_user(username, password)
        if user_doc:
            user_id = str(user_doc["_id"])
            print(f"User ID: {user_id}")
            self.auth_model.store_user_id(user_id)
            self.user_settings.set_logged_in_status(True)
            self.on_login_success()  # Notify the AppController of successful login and update its translation view UI
            self.login_view.destroy()  # Close the login view after successful login
            self.login_view = None
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password.")

    
    def logout(self):
        # Check if the login view is displayed and destroy it if it is
        if self.login_view and self.login_view.winfo_exists():
            self.login_view.destroy()
            self.login_view = None

        # Update the logged_in_status in the user settings
        self.user_settings.set_logged_in_status(False)

            # Update the login menu item
        self.root.nametowidget(self.menu_index_login).config(label="Log In")
        
        # Write the updated status to the .ini file
        self.user_settings.write_ini('Authentication', 'logged_in_status', 'False')
        
        # Optionally, show a confirmation message
        messagebox.showinfo("Logout", "You have successfully logged out.")

    def register_callback(self):
        self.display_register_view()

    def display_register_view(self):
        # Check if the login view is showing and destroy it
        if self.login_view and self.login_view.winfo_exists():
            self.login_view.destroy()
            self.login_view = None

        # Initialize self.register_view if it doesn't exist
        if not hasattr(self, 'register_view'):
            self.register_view = None

        # Create or show the register view
        if self.register_view is None or not self.register_view.winfo_exists():
            self.register_view = RegisterView(self.root, self.create_account_callback)
        else:
            self.register_view.deiconify()
            self.register_view.lift()

    def set_menu_indices(self, login_menu_index):
        print(f"Login menu index: {login_menu_index} in login_view_controller.py")
        self.menu_index_login = login_menu_index
        # Now you can update the menu label using this index
