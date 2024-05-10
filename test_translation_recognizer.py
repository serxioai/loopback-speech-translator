
import unittest
from unittest.mock import patch
from speech_session import AzureSpeechTranslateSession
import os

SUBSCRIPTION_KEY = os.environ.get("SPEECH_KEY")
SERVICE_REGION = os.environ.get("SPEECH_REGION")

class TestTranslationRecognizer(unittest.TestCase):

    @patch('azure.cognitiveservices.speech.SpeechTranslationConfig')
    @patch('azure.cognitiveservices.speech.TranslationRecognizer')
    def test_translation_recognizer_initialization(self, mock_recognizer, mock_config):
        # Setup your configuration values
        config = {
            'subscription_key':SUBSCRIPTION_KEY,
            'service_region': SERVICE_REGION    ,
            'speech_recognition_language': 'en-US'
        }

    session = AzureSpeechTranslateSession()

    # Create an instance of your class that initializes the recognizer
    instance = YourClass(config)
    instance.setup_translation_recognizer()

    # Check if SpeechTranslationConfig was called correctly
    mock_config.assert_called_with(subscription=config['subscription_key'],
                                    region=config['service_region'],
                                    speech_recognition_language=config['speech_recognition_language'])

    # Check if TranslationRecognizer was initialized with the right config
    mock_recognizer.assert_called_with(mock_config.return_value)

    # Optionally, check if the recognizer is in the correct state if applicable
    self.assertTrue(instance.translation_recognizer.is_properly_configured)
