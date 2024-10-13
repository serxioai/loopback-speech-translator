# app_controller.py

import tkinter as tk
from translation_view import TranslationView
from login_view import LoginView
from auth_model import AuthModel
from create_account_view import CreateAccountView
from menu_bar import MenuBar
from tkinter import messagebox
from azure_speech_translate_api import AzureSpeechTranslateAPI
from views.login_view_controller import LoginViewController

class AppController:
    def __init__(self, root, db, user_settings):
        self.root = root
        self.db = db
        self.user_settings = user_settings
        self.user_id = None
        self.db_manager = db
        self.auth_model = AuthModel()
        self.current_view = None
        self.logged_in_status = False
        self.initialized = False
        self.azure_speech_translate_api = None
        
        # Setup the login view controller
        self.setup_login_view_controller()

        # Setup the menu bar
        self.setup_menu_bar() 

        # Setup the Azure Speech Translate API
        self.initialize_azure_api()

        # Display the translation view
        self.launch_main_view()

    def setup_menu_bar(self):
        self.menu_bar = MenuBar(self.root, 
                                self.login_view_controller.display_login_view, 
                                self.user_settings)

    # Callback comes from views/login_view_controller.py
    def on_login_success(self):
        # Update translation view features UI
        self.menu_bar.update_login_menu_label('Log Out')

    # Callback comes from menu_bar.py
    def on_logout_success(self):
        messagebox.showinfo("You have been logged out.")
        self.menu_bar.update_login_menu_label('Log In')

    def launch_main_view(self):
        if self.current_view:
            self.current_view.destroy()

        TranslationView(
            self.root, 
            self.azure_speech_translate_api,
            self.user_settings,
        )
    
    def on_register(self):
        self.current_view = CreateAccountView(self.root, self.on_create_account)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def on_create_account(self, email, username, password):
        self.auth_model.register_user(email, username, password)
        self.display_login_view()

    def display_login_view(self):
        self.current_view = LoginView(self.root, self.on_login, self.on_register)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def initialize_azure_api(self):
        self.azure_speech_translate_api = AzureSpeechTranslateAPI(
            self.user_id, 
            self.db_manager,
        )
    def setup_login_view_controller(self):
        self.login_view_controller = LoginViewController(
            self.root, 
            self.user_settings, 
            self.on_login_success
        )

