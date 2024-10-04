import json

class Languages:
    def __init__(self):
        self.language_options = {}
        self.language_codes = {}
        self.load_language_options()

    def load_language_options(self):
        # Load the JSON file
        with open('languages.json', 'r') as file:
            self.language_options = json.load(file)

    def get_language_code_from_name(self, language_name):
        for language in self.language_options['languages']:
            if language['name'] == language_name:
                return language['language_code']
        return None  # Return None if the language name is not found
    
    def get_language_codes(self):
        for language in self.language_options['languages']:
            self.language_codes[language['name']] = language['language_code']
        return self.language_codes

    def get_language_code_from_locale(self, language_code):
        return self.language_options[language_code]
    
    def get_language_locale_from_name(self, language_name):
        for language in self.language_options['languages']:
            if language['name'] == language_name:
                return language['locale']
        return None  # Return None if the language name is not found

    def get_language_names(self):
        return [lang['name'] for lang in self.language_options['languages']]

    def get_language_options(self):
        return self.language_options
