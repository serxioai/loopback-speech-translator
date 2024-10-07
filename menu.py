import tkinter as tk
from tkinter import Menu

class MenuBar:
    def __init__(self, root):
        self.root = root
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
        translate_menu = Menu(menubar, tearoff=0)
        translate_menu.add_command(label='History')

        # add the Translation menu to the menubar
        menubar.add_cascade(label="Translation", menu=translate_menu, underline=0)

        # create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        self.root.config(menu=menubar)

        
