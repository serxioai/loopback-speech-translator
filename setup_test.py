from setuptools import setup
import os
import site
import sys
import azure.cognitiveservices.speech as speechsdk

# Get the exact paths we need
SITE_PACKAGES = site.getsitepackages()[0]
SPEECH_SDK_ROOT = os.path.dirname(speechsdk.__file__)

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'azure.cognitiveservices.speech'
    ],
    'includes': [
        'azure.cognitiveservices.speech',
        'azure.core'
    ],
    'excludes': [
        'azure'  # Exclude the deprecated meta-package
    ],
    'frameworks': [],
    'iconfile': None,
    'plist': {
        'CFBundleIdentifier': 'com.yourcompany.yourapp',
    },
    'site_packages': True,
}

# Add site packages to sys.path
if SITE_PACKAGES not in sys.path:
    sys.path.append(SITE_PACKAGES)

setup(
    name='YourApp',
    app=['test_azure.py'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 