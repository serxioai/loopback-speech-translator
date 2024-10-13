import tkinter as tk
from tkinter import Menu, ttk
from user_settings import UserSettings
from views.login_view import LoginView  # Import the LoginView
from tkinter import messagebox

class MenuBar:
    def __init__(self, root, display_login_view_cb, user_settings):
        self.root = root
        self.display_login_view_cb = display_login_view_cb
        self.user_settings = user_settings

        self._translate_menu = None  # Make translation menu a private member
        self._audio_menu = None
        self._login_menu_index = None   

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

        # Determine the label for the Log In/Log Out menu item
        self.file_menu.add_separator()
        login_label = 'Log Out' if self.user_settings.is_logged_in() else 'Log In'
        
        # Add Log In/Log Out menu item and store its index
        self.file_menu.add_command(label=login_label, command=self.handle_login_or_logout)
        self._login_menu_index = self.file_menu.index("end")  # Store the index of the login/logout item
        
        # Add Exit menu item
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit Kasana', command=self.root.destroy)

        # add the file menu to the menubar
        self.menubar.add_cascade(label="Settings", menu=self.file_menu)

        # create the Translation menu
        self.create_translation_menu(self.menubar)

        # create the Help menu
        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(label="Help", menu=help_menu)

    def handle_login_or_logout(self):
        if self.user_settings.is_logged_in():
            self.handle_log_out()
        else:
            self.handle_log_in()

    def handle_log_out(self):
        self.user_settings.set_logged_in_status(False)
        messagebox.showinfo("Logged Out", "You have been logged out.")
        self.update_login_menu_label('Log In')

    def handle_log_in(self):
        self.display_login_view_cb()

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

    def handle_login(self):
        if not self.user_settings.is_logged_in():
            # Display the login view using the callback from app_controller
            self.display_login_view()
    
    def update_login_menu_label(self, new_label):
        print(f"Print new label: {new_label} in menu_bar.py")
        print(f"Login menu index: {self._login_menu_index} UPDATE_LOGIN_MENU_LABEL in menu_bar.py")
        print(f"index type: {type(self._login_menu_index)}")
        # Update the label of the Log In/Log Out menu item using its index
        self.file_menu.entryconfig(self._login_menu_index, label=new_label)  # Ensure 'label' is used without a dash
