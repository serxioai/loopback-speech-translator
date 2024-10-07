from setuptools import setup

APP = ['kasana.py']  # Replace with the name of your main script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'Kasana',  # This changes the app name
        'CFBundleDisplayName': 'Kasana',
        'CFBundleIdentifier': 'com.lonestarinterpreting.kasana',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': True,  # This hides the dock icon for a menu-bar only app
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
