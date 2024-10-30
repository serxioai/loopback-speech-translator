# app_controller.py

import tkinter as tk
from translation_view import TranslationView
from create_account_view import CreateAccountView
from menu_bar import MenuBar
from azure_speech_translate_api import AzureSpeechTranslateAPI


class AppController:
    def __init__(self, root, user_settings):
        self.root = root
  
        self.user_settings = user_settings
        self.user_id = None
        self.current_view = None
        self.logged_in_status = False
        self.initialized = False
        self.azure_speech_translate_api = None
        
        # Setup the menu bar
        self.setup_menu_bar() 

        # Setup the Azure Speech Translate API
        self.initialize_azure_api()

        # Display the translation view
        self.launch_main_view()

    def setup_menu_bar(self):
        self.menu_bar = MenuBar(self.root, 
                                self.user_settings)

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

    def initialize_azure_api(self):
        self.azure_speech_translate_api = AzureSpeechTranslateAPI(
            self.user_id, 
        )

