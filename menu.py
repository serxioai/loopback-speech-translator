import tkinter as tk
from tkinter import Menu, ttk
from user_settings import UserSettings

class MenuBar:
    def __init__(self, root):
        self.root = root
        self.user_settings = UserSettings()
        self._translate_menu = None  # Make translation menu a private member
        self.audio_menu = None
        self.create_menubar()

    def create_menubar(self):
        # create a menubar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # create the file_menu
        file_menu = Menu(menubar, tearoff=0)

        # add menu items to the File menu
        file_menu.add_command(label='Feedback')
        file_menu.add_command(label='Privacy Policy')
        file_menu.add_separator()

        # add the Input Source menu
        self.create_input_source_menu(file_menu)

        # add Exit menu item
        file_menu.add_separator()
        file_menu.add_command(label='Quit Kasana', command=self.root.destroy)

        menubar.add_cascade(label="Settings", menu=file_menu, underline=0)

        # create the Translation menu
        self.create_translation_menu(menubar)

        # create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        self.root.config(menu=menubar)


    def create_translation_menu(self, menubar):
        # create the Translation menu
        self._translate_menu = Menu(menubar, tearoff=0)
        self._translate_menu.add_command(label='History')

        # create a menu for Save translations with check marks
        save_menu = Menu(self._translate_menu, tearoff=0)
        
        # Use a single BooleanVar to control both checkbuttons
        self.save_translations_var = tk.BooleanVar(value=self.user_settings.default_record_translations)
 
        save_menu.add_checkbutton(
            label="On",
            variable=self.save_translations_var,
            onvalue=True,
            offvalue=False,
            command=lambda: self.set_save_translations(True)
        )
        
        save_menu.add_checkbutton(
            label="Off",
            variable=self.save_translations_var,
            onvalue=False,
            offvalue=True,
            command=lambda: self.set_save_translations(False)
        )

        # add the Save menu to the Translation menu
        self._translate_menu.add_cascade(label="Save", menu=save_menu)
        # add the Translation menu to the menubar
        menubar.add_cascade(label="Translation", menu=self._translate_menu, underline=0)

    def create_input_source_menu(self, parent_menu):
        input_source_menu = Menu(parent_menu, tearoff=0)
        
        # Use a StringVar to control the radiobuttons
        self.audio_source_var = tk.StringVar(value=self.user_settings.get_audio_source())
        
        input_source_menu.add_radiobutton(
            label="Default Mic",
            variable=self.audio_source_var,
            value="default",
            command=lambda: self.set_audio_source("default")
        )
        
        input_source_menu.add_radiobutton(
            label="Video Conference Application",
            variable=self.audio_source_var,
            value="video_conference",
            command=lambda: self.set_audio_source("video_conference")
        )
        parent_menu.add_cascade(label="Input Source", menu=input_source_menu)

        # Update checkmarks based on current settings
        self.update_audio_source_checkmarks()

    def set_audio_source(self, source):
        self.user_settings.set_audio_source(source)
        # Update the INI file based on the selected source
        self.user_settings.write_ini('Audio Source', 'audio_source_default_mic', str(source == "default"))
        self.user_settings.write_ini('Audio Source', 'audio_source_video_conference', str(source == "video_conference"))
        
        # Update the checkmarks after changing the audio source
        self.update_audio_source_checkmarks()

    def update_audio_source_checkmarks(self):
        current_source = self.user_settings.get_audio_source()
        self.audio_source_var.set(current_source)

    def set_save_translations(self, value):
        if value:
            self.user_settings.set_default_record_translations(True)
        else:
            self.user_settings.set_default_record_translations(False)

