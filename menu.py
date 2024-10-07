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

        # add a submenu
        sub_menu = Menu(file_menu, tearoff=0)
        sub_menu.add_command(label='Default Mic (Bluetooth)')
        sub_menu.add_command(label='Videoconference Application')

        # add the File menu to the menubar
        file_menu.add_cascade(label="Input Source", menu=sub_menu)

        # add Exit menu item
        file_menu.add_separator()
        file_menu.add_command(label='Quit Kasana', command=self.root.destroy)

        menubar.add_cascade(label="Settings", menu=file_menu, underline=0)

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

        # create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        self.root.config(menu=menubar)

    def set_save_translations(self, value):
        if value:
            self.user_settings.set_default_record_translations(True)
        else:
            self.user_settings.set_default_record_translations(False)

