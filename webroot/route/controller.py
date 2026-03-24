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


LANG_KEY_PH_BISAYA  = ['ph-bis', 'bis', 'bisaya']


class Controller:
    
    def __init__(self, logger = None, model = None):
        self.TAG                = 'Model'
        
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

        

    
    def get_translation(self, lang_key):
        lower_lang_key = lang_key.lower()

        print('lang_key=' + lang_key);

        if lower_lang_key in LANG_KEY_PH_BISAYA:
            return self.translations['ph-bis']

        return None
    


    def set_view(self, view):
        self.view = view
        
        
        

        
        
        
        
