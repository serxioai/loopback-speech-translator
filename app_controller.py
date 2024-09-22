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

class AppController:
    def __init__(self, root, db_manager):
        self.user_id = None
        self.db_manager = db_manager
        self.root = root
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
        
        self.launch_translation_view()
    
    def launch_translation_view(self):
        if self.current_view:
            self.current_view.destroy()
        self.azure_speech_translate_api = AzureSpeechTranslateAPI(self.user_id, self.db_manager)
        self.current_view = TranslationView(
            self.root, 
            self.logged_in_status,
            self.on_start_audio_stream,
            self.on_stop_audio_stream,
            self.azure_speech_translate_api
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def launch_login_view(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginView(self.root, self.on_login, self.on_register)
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

    '''def launch_config_session_view(self) -> ConfigSessionView:
        self.clear_current_view()
        self.current_view = ConfigSessionView(self.root, 
                                               self.launch_translation_view)
        self.current_view.grid(row=0, column=0, sticky="nsew")'''
  
    '''def launch_translation_view(self, data):
        self.current_session = self.factory.init_session(data)
        self.clear_current_view()
        self.current_view = TranslationView(
            self.current_session,
            self.root, 
            self.on_start_audio_stream,
            self.on_stop_audio_stream,
        )
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_session.set_recognized_callback(self.update_recognized_translations)'''
      
    def update_recognized_translations(self):
        current_time = time.strftime("%H:%M:%S")    
        input_lang_code = self.current_session.languages['input']
        output_lang_code = self.current_session.languages['output']
        input_translation = self.current_session.get_recognized_translations(input_lang_code)
        output_translation = self.current_session.get_recognized_translations(output_lang_code)
        print(output_translation)
        self.current_session.save_translations(current_time, input_translation, output_translation)
        self.current_view.display_recognized_translations(current_time, input_translation, output_translation)

    def clear_current_view(self):
        if self.current_view:
            if hasattr(self.current_view, 'pack_forget'):
                self.current_view.pack_forget()
            elif hasattr(self.current_view, 'grid_forget'):
                self.current_view.grid_forget()
            self.current_view.destroy()
            self.current_view = None

    def on_start_audio_stream(self):
        if self.current_session:
            self.current_session.start()

    def on_stop_audio_stream(self):
        if self.current_session:
            self.current_session.stop()

    def logout(self):
        self.auth_model.clear_stored_user_id()
        self.user_id = None
        self.factory.set_user_id(None)
        self.launch_login_view()