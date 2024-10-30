from setuptools import setup

APP = ['kasana.py']
DATA_FILES = [
    'settings.ini',
    '.env'  # Make sure this is included for your credentials
]

OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'tkinter',
        'azure.cosmos',
        'azure.cognitiveservices.speech',
        'bcrypt',
        'dotenv'
    ],
    'plist': {
        'CFBundleName': 'Kasana',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.yourdomain.kasana',
        'NSMicrophoneUsageDescription': 'Kasana needs access to your microphone for speech translation.',
        'LSMinimumSystemVersion': '10.10',
    }
}

setup(
    name='Kasana',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'azure-cosmos>=4.0.0',
        'azure-cognitiveservices-speech>=1.25.0',
        'python-dotenv>=0.19.0',
        'bcrypt>=4.0.1'
    ],
)
