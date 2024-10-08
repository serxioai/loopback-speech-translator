# app_controller.py

import tkinter as tk
import webbrowser
import os
from translation_view import TranslationView
from login_view import LoginView
from auth_model import AuthModel
from create_account_view import CreateAccountView
from auth_model import AuthModel
import time
from azure_speech_translate_api import AzureSpeechTranslateAPI

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse as urlparse
import configparser

class AppController:
    def __init__(self, root, db, user_settings):
        self.root = root
        self.db = db
        self.user_settings = user_settings
        self.user_id = None
        self.db_manager = db
        self.auth_model = AuthModel()
        self.current_view = None
        self.current_session = None
        self.logged_in_status = False
        self.check_login_status()  # Call this instead of directly launching translation view
        self.display_translation_view()

    def check_login_status(self):
        # Check if there's a stored user session
        stored_user_id = self.auth_model.get_stored_user_id()
        if stored_user_id:
            self.user_id = stored_user_id
            self.user_settings.set_logged_in_status(True)
        else:
            self.user_settings.set_logged_in_status(False)     

    def update_logged_in_status_in_settings(self, status):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        
        if 'Settings' not in config:
            config['Settings'] = {}
        
        config['Settings']['logged_in_status'] = str(status)
        
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def display_translation_view(self):
        if self.current_view:
            self.current_view.destroy()
        
        self.azure_speech_translate_api = AzureSpeechTranslateAPI(
            self.user_id, 
            self.db_manager,
        )

        TranslationView(
            self.root, 
            self.azure_speech_translate_api,
            self.user_settings,
        )

    def display_login_view(self):
        LoginView(self.root, self.on_login, self.on_register)
        # No need to pack or grid the LoginView, as it's a Toplevel window

    def on_login(self, username, password):
        user_doc = self.auth_model.authenticate_user(username, password)
        if user_doc:
            user_id = str(user_doc["_id"])
            self.user_id = user_id
            self.auth_model.store_user_id(user_id)
            self.user_settings.set_logged_in_status(True)
            self.display_translation_view()
        else:
            print("Authentication failed")
    
    def on_register(self):
        self.current_view = CreateAccountView(self.root, self.on_create_account)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def on_create_account(self, email, username, password):
        self.auth_model.register_user(email, username, password)
        self.display_login_view()

    def logout(self):
        pass