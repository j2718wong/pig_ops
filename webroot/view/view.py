__author__ = "Jack Wong j2718wong@gmail.com"
__date__ = "2025-10-01 10:00:00"


import sys
import os
import json
import pprint

from pathlib                import Path


"""
2025-12-23 Notes
1.) Up until to this date, the focus of development was desktop web recycling 
old front end technologies.

2.) After this date, the new focus will be on mobile web first which is 
drastically a different version of the desktop version.

3.) There will be two repos to be maintained until both the mobile and desktop 
versions are integrated.


 
"""



# Include the directory where this file is located 
module_file_path        = os.path.abspath(__file__)
module_directory        = os.path.dirname(module_file_path)
webroot_directory       = os.path.dirname(module_directory)


if module_directory not in sys.path:
   sys.path.append(module_directory)


from jinja2             import Environment, FileSystemLoader

from common_fast_api    import dir_static, dir_static_m, dir_admin_static, get_application_data


from datetime           import datetime


# Set up the Jinja environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('templates'))


view_names = [
            ('signup',              'SignUp'),
            ('contact',             'Contact'),
            
            ('privacy',             'Privacy'),
            ('terms',               'Terms'), 
            
            ('receipts',            'AdminReceipts'),
            
            ('root',                'Root')            
        ]


PAGE_TYPE_LOGIN             = 'login'
PAGE_TYPE_CORE_APP          = 'core'
PAGE_TYPE_RECEIPT_DATA      = 'receipt_data_entry'


class View:
    def __init__(self, controller):
        controller.set_view(self)
        self.controller = controller

        self.views = {}
        for view_name in view_names:
            self.views[view_name[0]] = globals()[view_name[1]](self)


    def __getitem__(self, view_name):
        return self.views[view_name]



class ViewBase:
    def __init__(self, view):
        self.view = view
        self.controller = view.controller
        
        # SPA (Farmer App) paths
        self.manifest_path      = dir_static + '/js/manifest.json'
        self.css_manifest_path  = dir_static + '/css/manifest.json'
        
        # Admin App paths
        self.admin_manifest_path = dir_admin_static + '/js/manifest.json'
        
        self.default_manifest = {
            'login':                'bundle.min.js',
            'core':                 'bundle.core.min.js',
            'receipt_data_entry':   'bundle.receipt_data_entry.min.js',  
            'main_css':             'main.min.css'
        }
        
    
    
    def get_js_files(self, page_type=PAGE_TYPE_CORE_APP):
        """
        Return appropriate JS files based on environment
        """
        # Admin pages use separate build
        if page_type == PAGE_TYPE_RECEIPT_DATA:
            return self._get_admin_js_files(page_type)
        
        if self.controller.use_minified_js > 0:
            return self._get_prod_js_files(page_type)
        
        return self._get_dev_js_files(page_type)
    
    
    def _get_admin_js_files(self, page_type=PAGE_TYPE_RECEIPT_DATA):
        """
        Get admin app JS files (separate from SPA)
        """
        if self.controller.use_minified_js == 0:
            # Development: use source file from admin repo
            return {
                'text':    [],
                'module':  ["/admin/dev/js/app_receipt_data_entry.js"]
            }
        else:
            # Production: use minified bundle with versioning
            try:
                if os.path.exists(self.admin_manifest_path):
                    with open(self.admin_manifest_path, 'r') as f:
                        manifest = json.load(f)
                    
                    filename = manifest.get(page_type, self.default_manifest.get(page_type, 'bundle.receipt_data_entry.min.js'))
                    
                    return {
                        'text':    [f"/admin/static/js/{filename}"],
                        'module':  []
                    }
            except Exception as e:
                print(f"Error reading admin manifest: {e}")
            
            # Fallback to non-versioned file
            return {
                'text':    ["/admin/static/js/bundle.receipt_data_entry.min.js"],
                'module':  []
            }
    
    
    def _get_prod_js_files(self, page_type=PAGE_TYPE_CORE_APP):
        """Production: just the minified bundle for SPA"""
        try:
            if os.path.exists(self.manifest_path):
                with open(self.manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                filename = manifest.get(page_type, self.default_manifest[page_type])
                
                return {
                    'text':    [f"/static/js/{filename}"],
                    'module':  []
                }
        except:
            pass
        
        return {
            'text':    [f"/static/js/{self.default_manifest[page_type]}"],
            'module':  []
        }
    
    
    def _get_dev_js_files(self, page_type=PAGE_TYPE_CORE_APP):
        """Development: return all individual modules for debugging"""
        if page_type == PAGE_TYPE_LOGIN:
            return {
                'text':    [],
                'module':  ["/static_m/js/app.js"]
            }
        
        if page_type == PAGE_TYPE_CORE_APP:
            return {
                'text':     [],
                'module':  ["/static_m/js/app_core.js"]
            }
        
        if page_type == PAGE_TYPE_RECEIPT_DATA:
            # This shouldn't reach here anymore (handled by _get_admin_js_files)
            return {
                'text':     [],
                'module':  ["/admin/dev/js/app_receipt_data_entry.js"]
            }
        
        # Default fallback
        return {
            'text':     [],
            'module':   []
        }
    
    def get_manifest(self):
        """Always read manifest from disk for SPA"""
        manifest_path = dir_static + '/js/manifest.json'
        
        try:
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading manifest: {e}")
        
        return {
            'login': 'bundle.min.js',
            'core': 'bundle.core.min.js'
        }
    
    
    def get_admin_manifest(self):
        """Read admin app manifest"""
        try:
            if os.path.exists(self.admin_manifest_path):
                with open(self.admin_manifest_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading admin manifest: {e}")
        
        return {
            'receipt_data_entry': 'bundle.receipt_data_entry.min.js'
        }
    
    
    def get_css_manifest(self):
        """Get CSS manifest - separate for CSS versioning"""
        try:
            if os.path.exists(self.css_manifest_path):
                with open(self.css_manifest_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading CSS manifest: {e}")
        
        return {
            'main_css': 'main.min.css'
        }
    
    
    def get_css_files(self):
        """
        Return appropriate CSS files based on environment
        """
        if self.controller.use_minified_js > 0:
            manifest = self.get_css_manifest()
            css_file = manifest.get('main_css', self.default_manifest['main_css'])
            return [f"/static/css/{css_file}"]
        else:
            return ["/static_m/css/main.css"]
    
    
    

class SignUp(ViewBase):
    def render(self, lang = 'en', translations = None, available_languages = None ):
        
        # Mobile version
        template = env.get_template('signup.html')
        
        # Get appropriate JS files based on environment
        files = self.get_js_files(PAGE_TYPE_LOGIN)
        
        # Get app_ui_settings
        ui_settings     = self.controller.get_app_ui_settings()
        app_ui_settings = json.dumps(ui_settings)

        app_version = self.controller.APP_VERSION
        
        
        page_data = {
            'app_version':          app_version,
            'app_ui_settings':      app_ui_settings,
            'lang':                 lang,
            'translations':         translations,
            'available_languages':  available_languages
        }
        
            
        data    = { 'page_data':        page_data,
                    'js_lib':           [],
                    'js_app_text':      files['text'],
                    'js_app_modules':   files['module']
                    }
        
                
        return template.render(data)
   
   
class Privacy(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('privacy.html')
        
        application_data = get_application_data()
        
        current_year    = datetime.now().year
        
        
        page_data ={
            
            'current_year':         current_year,
            'contact_email':        application_data['contact_email'],
            'privacy_officer':      application_data['privacy_officer'],
            'privacy_email':        application_data['privacy_email'],
            
            'eu_privacy_officer':   application_data['eu_privacy_officer'],
            'eu_privacy_email':     application_data['eu_privacy_email'],
            'eu_representrative':   application_data['eu_representrative']
        }
        
            
        data    = { 'page_data':        page_data}
        
                
        return template.render(data)
   


class Contact(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('contact.html')
        
        application_data = get_application_data()
        
        current_year    = datetime.now().year
        
        
        page_data ={
            'app_version':          self.controller.APP_VERSION,
            'current_year':         current_year,
            'contact_email':        application_data['contact_email'],
            'contact_whatsapp':     application_data['contact_whatsapp']
        }
        
            
        data    = { 'page_data':        page_data}
        
                
        return template.render(data)



class Terms(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('terms.html')
        
        application_data = get_application_data()
        
        current_year    = datetime.now().year
        
        
        page_data ={
            
            
        }
        
            
        data    = { 'page_data':        page_data}
        
                
        return template.render(data)



class AdminReceipts(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('admin_receipts.html')
        
        application_data = get_application_data()
        
        current_year    = datetime.now().year
        
        # Get appropriate JS files for receipt data entry
        files = self.get_js_files(PAGE_TYPE_RECEIPT_DATA)
        
        css_files   = []
        js_lib      = []
        
        page_data ={
            'app_version':          self.controller.APP_VERSION
        }
        
            
        data    = { 'page_data':        page_data,
                    'css_files':        css_files,
                    'js_lib':           js_lib,
                    'js_app_text':      files['text'],
                    'js_app_modules':   files['module'],
        
        }
        
                
        return template.render(data)



    
#
# Views
#



# Map language to image folder
lang_image_map = {
    'en':  'mar',
    'zh':  'mar_zh',
    'tag': 'mar_tag',
    'ceb': 'mar_ceb'
}


# Add a helper function to check if a static file exists
def static_file_exists(relative_path):
    """
    Check if a static file exists in the static_m directory
    relative_path: e.g., "images/mar_zh/mar_home.png"
    """
    try:
        full_path = os.path.join(dir_static_m, relative_path)
        return os.path.exists(full_path)
    except Exception as e:
        print(f"Error checking static file: {e}")
        return False


"""
2026-04-02: Notes on translations
1.) There are several sets for translations

Translations for public pages; user not yet logged in
=====================================================
- only for end points /  /login /signup
- including subsequent pages after signup; generally pages
  rendered via ManagerLogin JS class

- For / end point (home page), the translations to home page are
 loaded via jinja templates, because the home page of different languages 
  needs to be searchable by search engines
  
- For /login and /signup   are rendered by JS and the translated contents
 are loaded via JS. Therefore these pages are not searchable by search engines 

- the translations are located in
dev01@raspberrypi:~/projects/jsys/pig_ops/webroot/templates $ tree
.
├── content
│   ├── carousel.json
│   └── marketing_highlights.json
└── translations
    ├── ceb.json
    └── en.json

- the content directory is for home page translation with images
  and variable contents items. 

- the translations directory are for text translations


- the translated images are located in 

dev01@raspberrypi:~/projects/jsys/pig_ops_ui_mob/src/static/images $ tree
.
├── box_check.png
├── mar
│   ├── mar_fattening.png
│   ├── mar_feed_records.png
│   ├── mar_gesta.png
│   ├── mar_home.png
│   ├── mar_lacta.png
│   ├── mar_pig_ops.png
│   ├── mar_report.png
│   └── mar_sow_list.png
├── mar_bis
└── mar_tag




Translations for user already logged in  including reports generation.
=====================================================================
- this is located in 

dev01@raspberrypi:~/projects/jsys/pig_ops/webroot/locale $ tree
.
└── locale_bisaya.json


- There is no translation for english as the english text are hardcoded
in html templates or JS page classes

"""




class Root(ViewBase):
    

    
    def render(self, uhid = None, translation = None, lang = None,
            available_languages = None, return_spa_app = 0):
        """
        Will render 
        
        if return_spa_app > 0:
            return SPA, regardless user is logged in or not; 
        
        else:
            if uhid is None:
                should return home page; user not logged in
            
            else:
                should return SPA; user is logged in
                
        Parameters
        ----------
        
        uhid : string
            user_id hid
            
        translation : dictionary
            if uhid is not None:
                This is the translation to be used when user is ALREADY logged in;
                if None, the user logged in pages will use the default 
                english text hardcoded via JS or HTML.
                
            if uhid is None:
                this is ignored;
                
            
            
        lang : str
            language key for user not logged in 
        
        available_languages : list of dictionaries for available languages 
            for drop down
        """
        
        if lang is None:
            lang = 'en'
        
        
        # Get the language to be displayed
        language_display = 'English'
        if available_languages is not None:
            for cur_entry in available_languages:
                if 'active' in cur_entry and cur_entry['active']:
                    language_display = cur_entry['local_name']
                    break
        else:
            available_languages = [{'code': 'en', 
                                    'url': '/en', 
                                    'name': 'English', 
                                    'local_name': 'English', 
                                    'active': True}]
        
        
        
        # Get app_ui_settings
        ui_settings     = self.controller.get_app_ui_settings()
        app_ui_settings = json.dumps(ui_settings)
            
        
        RETURN_HOME_PAGE    = 0
        RETURN_SPA_APP      = 1
        
        return_page = RETURN_HOME_PAGE
        
        if return_spa_app > 0:
            return_page = RETURN_SPA_APP
        else:
            if uhid is not None:
                return_page = RETURN_SPA_APP
        
        
        if return_page == RETURN_SPA_APP:
            # Mobile version
            template = env.get_template('index_mob.html')
            
            # Get appropriate JS files based on environment
            files = self.get_js_files(PAGE_TYPE_CORE_APP)
            
            css_files = self.get_css_files()
            
            
            # These should have type= text/javascript
            js_lib  = []
            
            

            s_translation = None
            if translation is not None:
                # This is a json string  to be attached to HTML template
                s_translation = json.dumps(translation)
            
            
            vapid_public_key    = self.controller.vapid_public_key
            
            
            page_data = {
                'app_version':              self.controller.APP_VERSION,
                'app_ui_settings':          app_ui_settings,
                'vapid_public_key':         vapid_public_key
            }
            
            
                
            data    = { 'page_data':        page_data,
                        'css_files':        css_files,
                        'js_lib':           js_lib,
                        'js_app_text':      files['text'],
                        'js_app_modules':   files['module'],
                        'translation':      s_translation
                    }
            
                    
            return template.render(data)
            
        else:
            # Public homepage for non-logged-in users
            
            
            app_version = self.controller.APP_VERSION
            
            
            # Load carousel from JSON with language support
            carousel_items  = self.load_carousel_with_lang(lang, app_version)
            
            # Load marketing items
            marketing_items = self.load_marketing_highlights_with_lang(lang)
            
            
            page_data = {
                'app_version':          app_version,
                'app_ui_settings':      app_ui_settings,
                
                'lang':                 lang,
                'language_display':     language_display,
                'available_languages':  available_languages,
            
                'carousel':             carousel_items,
                'marketing_highlights': marketing_items
            }
            
            
            # Mobile version
            template = env.get_template('home.html')
            
            
            # Get appropriate JS files based on environment
            js_app_text = []
            
            
            # These should have type= text/javascript
            js_lib  = []
            
        
            # These should have type= module
            js_app_modules = []
            
            print('view lang = %s' % lang)
            
            # Get public pages translations once; this is a dictionary object
            public_pages_trans    = self.controller.get_public_pages_translations(lang)
            public_pages_trans_en = self.controller.get_public_pages_translations('en')
            
            
    
            
            
            # Get home translation; This is populated via jinja templates
            home_translation = None
            
            if public_pages_trans is None:
                public_pages_trans  = public_pages_trans_en
                home_translation    = public_pages_trans_en['page_home']
            else:
                home_translation    = public_pages_trans['page_home']
            
            
            # Remove page_home from public_pages 
            del public_pages_trans['page_home']
            
            # Add available_languages to public_pages_trans
            public_pages_trans['available_languages'] = available_languages 
            
                
            data    = { 'page_data':        page_data,
                        'js_lib':           js_lib,
                        'js_app_text':      js_app_text,
                        'js_app_modules':   js_app_modules,
                        'home_translation': home_translation
                    }
            
                    
            return template.render(data)


    def load_carousel_with_lang(self, lang='en', app_version=''):
        """Load carousel items with language-specific images, fallback to English"""
        
        # Get image folder for this language, fallback to English
        image_folder = lang_image_map.get(lang, 'mar')
        default_folder = 'mar'  # English folder
        
        # Load base carousel structure
        carousel_base = self.load_carousel()
        
        # Get translations for this language
        translations    = self.controller.get_public_pages_translations(lang)
        translations_en = self.controller.get_public_pages_translations('en')
        
        page_home       = translations.get('page_home', {})
        page_home_en    = translations_en.get('page_home', {})
        
        # Pre-fetch translations
        carousel_items_trans    = page_home.get('carousel', {}).get('items', {})
        carousel_items_trans_en = page_home_en.get('carousel', {}).get('items', {})
        
        carousel_items = []
        
        for item in carousel_base:
            image_key   = item.get('image_key', '')
            text_key    = item.get('key', '')
            
            # Get title and description
            title   = carousel_items_trans.get(text_key, {}).get('title', '')
            desc    = carousel_items_trans.get(text_key, {}).get('desc', '')
            
            if not title:
                title   = carousel_items_trans_en.get(text_key, {}).get('title', image_key)
                desc    = carousel_items_trans_en.get(text_key, {}).get('desc', '')
            
            # Check if localized image exists
            lang_relative_path = f"images/{image_folder}/{image_key}.png"
            default_relative_path = f"images/{default_folder}/{image_key}.png"
            
            # Use controller's method to check if file exists
            if static_file_exists(lang_relative_path):
                img_path = f"/static_m/{lang_relative_path}"
            else:
                img_path = f"/static_m/{default_relative_path}"
                # Optional: log missing image
                # print(f"Missing image: {lang_relative_path}, using default")
            
            carousel_items.append({
                'img_path': f"{img_path}?v={app_version}",
                'title': title,
                'desc': desc
            })
        
        return carousel_items
        
        
    def load_carousel(self):
        """Load carousel items from JSON file"""
        try:
            filepath = os.path.join(webroot_directory, "templates/content/carousel.json")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("items", [])
        except Exception as e:
            print(f"Error loading carousel: {e}")
            return []


    def load_marketing_highlights_with_lang(self, lang='en'):
        """Load marketing highlights with language-specific text, fallback to English"""
        
        # Load base structure
        highlights_base = self.load_marketing_highlights()
        
        # Get translations once
        translations    = self.controller.get_public_pages_translations(lang)
        translations_en = self.controller.get_public_pages_translations('en')
        
        page_home       = translations.get('page_home', {})
        page_home_en    = translations_en.get('page_home', {})
        
        # Pre-fetch highlights translations
        highlights_trans    = page_home.get('highlights', {}).get('items', {})
        highlights_trans_en = page_home_en.get('highlights', {}).get('items', {})
        
        marketing_items = []
        
        for item in highlights_base:
            text_key = item.get('key', '')
            
            # Get translated text
            title = highlights_trans.get(text_key, {}).get('title', '')
            desc = highlights_trans.get(text_key, {}).get('desc', '')
            
            # Fallback to English
            if not title:
                title = highlights_trans_en.get(text_key, {}).get('title', '')
                desc = highlights_trans_en.get(text_key, {}).get('desc', '')
            
            # Final fallback to original JSON
            if not title:
                title = item.get('title', '')
                desc = item.get('desc', '')
            
            marketing_items.append({
                'title': title,
                'desc': desc
            })
        
        return marketing_items


    def load_marketing_highlights(self):
        """Load marketing highlights from JSON file"""
        try:
            filepath = os.path.join(webroot_directory, "templates/content/marketing_highlights.json")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("items", [])
        except Exception as e:
            print(f"Error loading marketing highlights: {e}")
            return []

