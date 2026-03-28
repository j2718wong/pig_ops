# November 27, 2025
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys
import json
import pprint


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)
webroot_directory           = os.path.dirname(module_directory)


# Add route directory to Python path
locale_dir = os.path.join(webroot_directory, 'locale')
if locale_dir not in sys.path:
    sys.path.insert(0, locale_dir)


TRANSLATED_LANGUAGES = [
    {'key': 'en',       'lang_input': ['default', 'en', 'english']},

    {'key': 'ph-bis',   'lang_input': ['ph-bis', 'bis', 'bisaya', 'ceb']},
    {'key': 'ph-tag',   'lang_input': ['ph-tag', 'tag', 'tagalog']}

]



class Controller:
    
    def __init__(self, logger = None, model = None):
        self.TAG                = 'Model'

        self.APP_VERSION        = ''
        
        self.is_prod_envi       = False
        
        self.use_minified_js    = 1
        
        self.logger             = logger
        
        self.model              = model
        
        
        self.view               = None
        

        self.translations       = {}
        
        self.load_translations()

        
    def load_translations(self):
        
        # Load Bisaya
        abspath_ph_bis = os.path.join(locale_dir, 'locale_bisaya.json')

        f = open(abspath_ph_bis, 'r', encoding='utf-8')
        s = f.read();
        f.close();
        
        translation = None
        try:
            translation = json.loads(s)
        except Exception as e:
            print('Error Loading translation: ' + str(e))

        
        if translation is not None:
            self.translations['ph-bis'] = translation

    
    def get_language_key(self, input_lang):
        """
        Convert user input language (e.g., 'bis', 'bisaya', 'en') to internal language key
        Returns the language key or None if not found
        """
        if input_lang is None:
            return None
            
        input_lang_lower = input_lang.lower().strip()
        
        # Loop through TRANSLATED_LANGUAGES to find matching input
        for lang_entry in TRANSLATED_LANGUAGES:
            for lang_input in lang_entry['lang_input']:
                if lang_input == input_lang_lower:
                    return lang_entry['key']
        
        return None


    
    def get_translation(self, language_key):
        """
        Returns the translation dictionary for the given language key
        Returns None if no translation exists (use default English from frontend)
        """
        if language_key is None:
            return None
            
        
        # Check if translation exists for this language key
        if language_key in self.translations:
            return self.translations[language_key]
        
        # No translation found - frontend will use default English
        return None
    


    def set_view(self, view):
        self.view = view
        
        
        

        
        
        
        
