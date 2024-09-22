import unittest
from unittest import TestCase, mock
from azure.cognitiveservices.speech import SpeechRecognizer
from azure_speech_translate_api import AzureSpeechTranslateSession

class TestSpeechRecognition(TestCase):
    def test_cancellation_handling(self):
        # Create a mock recognizer
        recognizer = mock.create_autospec(SpeechRecognizer)
        
        # Assuming `SpeechConnection` is your class handling the recognizer
        connection = AzureSpeechTranslateSession('00000001', config_data)
        connection.translation_recognizer = recognizer

        # Simulate the cancellation handling
        with mock.patch.object(connection, 'on_canceled') as mock_on_canceled:
            recognizer.canceled.connect.assert_called_once_with(mock_on_canceled)
            recognizer.canceled.fire()  # Manually fire the canceled event

            # Check if the handling function is called
            mock_on_canceled.assert_called_once()


if __name__ == '__main__':
        unittest.main()