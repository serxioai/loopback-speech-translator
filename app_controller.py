# app_controller.py

import tkinter as tk
import webbrowser
import os
from translation_view import TranslationView
from login_view import LoginView
from auth_model import AuthModel
from create_account import CreateAccount
from auth_model import AuthModel
import time
from azure_speech_translate_api import AzureSpeechTranslateAPI

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse as urlparse
import configparser

class AppController:
    def __init__(self, root, db, settings):
        self.root = root
        self.db = db
        self.settings = settings
        self.audio_source = settings["audio_source"]
        self.speech_detection_language = settings["speech_detection_language"]
        self.user_id = None
        self.db_manager = db
        self.auth_model = AuthModel()
        self.current_view = None
        self.current_session = None
        self.logged_in_status = False
        self.check_login_status()  # Call this instead of directly launching translation view

    def check_login_status(self):
        # Check if there's a stored user session
        stored_user_id = self.auth_model.get_stored_user_id()
        if stored_user_id:
            self.user_id = stored_user_id
            self.logged_in_status = True
        else:
            self.logged_in_status = False
        
        # Update the settings.ini file
        self.update_logged_in_status_in_settings(self.logged_in_status)
        
        self.launch_translation_view()

    def update_logged_in_status_in_settings(self, status):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        
        if 'Settings' not in config:
            config['Settings'] = {}
        
        config['Settings']['logged_in_status'] = str(status)
        
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def launch_translation_view(self):
        if self.current_view:
            self.current_view.destroy()
        
        self.azure_speech_translate_api = AzureSpeechTranslateAPI(
            self.user_id, 
            self.db_manager,
        )

        TranslationView(
            self.root, 
            self.logged_in_status,
            self.azure_speech_translate_api,
            self.settings,
        )

    def launch_login_view(self):
        LoginView(self.root, self.on_login, self.on_register)
        # No need to pack or grid the LoginView, as it's a Toplevel window

    def on_login(self, username, password):
        user_doc = self.auth_model.authenticate_user(username, password)
        if user_doc:
            user_id = str(user_doc["_id"])
            self.user_id = user_id
            self.auth_model.store_user_id(user_id)
            self.launch_translation_view()
        else:
            print("Authentication failed")
    
    def on_register(self):
        self.clear_current_view()
        self.current_view = CreateAccount(self.root, self.on_create_account)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def on_create_account(self, email, username, password):
        self.auth_model.register_user(email, username, password)
        self.launch_login_view()
      
    def on_display_completed_translation(self):
        current_time = time.strftime("%H:%M:%S")    
        input_lang_code = self.settings.languages['input']
        output_lang_code = self.settings.languages['output']
        input_translation = self.azure_speech_translate_api.get_recognized_translations(input_lang_code)
        output_translation = self.azure_speech_translate_api.get_recognized_translations(output_lang_code)
        self.azure_speech_translate_api.save_translations(current_time, input_translation, output_translation)

    def logout(self):
        pass