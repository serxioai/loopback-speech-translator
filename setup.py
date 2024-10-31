from setuptools import setup

APP = ['kasana.py']
DATA_FILES = [
    'settings.ini',
    '.env'  # Make sure this is included for your credentials
]

OPTIONS = {
    'argv_emulation': False,
    'frameworks': [],
}

setup(
    name='Kasana',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'azure-cognitiveservices-speech>=1.25.0',
        'python-dotenv>=0.19.0',
    ],
)
