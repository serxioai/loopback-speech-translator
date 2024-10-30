import tkinter as tk
from tkinter import messagebox, Menu

class MenuBar:
    def __init__(self, root, user_settings):
        """
        Initialize the MenuBar.

        Args:
            root (tk.Tk): The root window of the application
            user_settings (UserSettings): User settings instance
        """
        self.root = root
        self.user_settings = user_settings
        self._audio_menu = None

        self.create_menubar()

    def create_menubar(self):
        # create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # create the file_menu
        self.file_menu = Menu(self.menubar, tearoff=0)

        # add menu items to the File menu
        self.file_menu.add_command(label='Feedback')
        self.file_menu.add_command(label='Privacy Policy')
        self.file_menu.add_separator()

        # add the Input Source menu
        self.create_input_source_menu(self.file_menu)
        
        # Add Exit menu item
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit Kasana', command=self.root.destroy)

        # add the file menu to the menubar
        self.menubar.add_cascade(label="Settings", menu=self.file_menu)

        # create the Help menu
        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(label="Help", menu=help_menu)

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
