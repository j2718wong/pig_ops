__author__ = "Jack Wong j2718wong@gmail.com"
__date__ = "2025-10-01 10:00:00"


import sys
import os
import json
import pprint



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

if module_directory not in sys.path:
   sys.path.append(module_directory)


from jinja2             import Environment, FileSystemLoader

from common_fast_api    import dir_static, dir_static_m, get_application_data


from datetime           import datetime


# Set up the Jinja environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('templates'))


view_names = [
            ('signup',              'SignUp'),
            
            ('privacy',             'Privacy'),
            ('terms',               'Terms'), 
            ('root',                'Root')            
        ]


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
        
        self.manifest_path      = dir_static + '/js/manifest.json'
        self.css_manifest_path  = dir_static + '/css/manifest.json'
        self.default_manifest   = {
            'login':    'bundle.min.js',
            'core':     'bundle.core.min.js',
            'main_css': 'main.min.css'  # Default CSS fallback
        }
        
        self.is_dev = False
        
        if self.controller.is_prod_envi == False:
            self.is_dev = True
      
    
    
    
    def get_js_files(self, page_type='core'):
        """
        Return appropriate JS files based on environment
        """
        if self.is_dev == True:
            # DEVELOPMENT: Return all individual modules for easy debugging
            return self._get_dev_js_files(page_type)
        else:
            # PRODUCTION: Return minified bundle
            if self.controller.use_minified_js > 0:
                return self._get_prod_js_files(page_type)
            
            # Overide to not to use minified JS
            return self._get_dev_js_files(page_type)
            
            
    
    def _get_prod_js_files(self, page_type='core'):
        """Production: just the minified bundle"""
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
        
        
    
    def _get_dev_js_files(self, page_type='core'):
        """Development: return all individual modules for debugging"""
        if page_type == 'login':
            # Login page modules
            return {
                'text':    [],
                'module':  ["/static_m/js/app.js"]
            }
            
        else:  # core/dashboard
            # Core navigation and all other modules
            return {
                'text':     [],
                'module':  ["/static_m/js/app_core.js"]
            }
    
    
    def get_manifest(self):
        """Always read manifest from disk - simplest, always fresh"""
        manifest_path = dir_static + '/js/manifest.json'
        
        try:
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading manifest: {e}")
        
        # Fallback defaults
        return {
            'login': 'bundle.min.js',
            'core': 'bundle.core.min.js'
        }
    
    
    def get_css_manifest(self):
        """Get CSS manifest - separate for CSS versioning"""
        try:
            if os.path.exists(self.css_manifest_path):
                with open(self.css_manifest_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading CSS manifest: {e}")
        
        # Fallback defaults
        return {
            'main_css': 'main.min.css'
        }
    
    
    def get_css_files(self):
        """
        Return appropriate CSS files based on environment
        Returns list of CSS files to include
        """
        if self.is_dev:
            # DEVELOPMENT: Return original CSS for debugging
            return ["/static_m/css/main.css"]
        else:
            # PRODUCTION: Return versioned/minified CSS
            if self.controller.use_minified_js > 0:
                manifest = self.get_css_manifest()
                css_file = manifest.get('main_css', self.default_manifest['main_css'])
                return [f"/static/css/{css_file}"]
            else:
                # Override to use unminified CSS
                return ["/static_m/css/main.css"]
    
    
    

class SignUp(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('signup.html')
        
        # Get appropriate JS files based on environment
        files = self.get_js_files('login')
        
            
        data    = { 'page_data':        page_data,
                    'js_lib':           [],
                    'js_app_text':      files['text'],
                    'js_app_modules':   files['module'],
                    'is_dev':           self.is_dev}
        
                
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


   
    
#
# Views
#


class Root(ViewBase):
    def render(self, uhid = None, translation = None):
        
        
        if uhid is not None:
            # Mobile version
            template = env.get_template('index_mob.html')
            
            # Get appropriate JS files based on environment
            files = self.get_js_files('core')
            
            css_files = self.get_css_files()
            
            
            # These should have type= text/javascript
            js_lib  = []
            
            

            s_translation = None
            if translation is not None:
                s_translation = json.dumps(translation)
            
            
            
            
            page_data = {
                'app_version':              self.controller.APP_VERSION
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
            
            app_version = self.controller.APP_VERSION
            
            
            page_data = {
                'app_version':              app_version,
            
                'carousel':[
                    {
                        'img_path': '/static_m/images/mar/mar_home.png?v=%s' % app_version,
                        'title': 'Dashboard Overview',
                        'desc': 'Real-time pig farm metrics and KPIs at your fingertips'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_sow_list.png?v=%s' % app_version,
                        'title': 'Sow Management',
                        'desc': 'Manage your breeding sows, boars and gilts'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_gesta.png?v=%s' % app_version,
                        'title': 'Breeding Cycles Management',
                        'desc': 'Track gestation, lactation, and breeding cycles'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_lacta.png?v=%s' % app_version,
                        'title': 'Pig Operations Management',
                        'desc': 'Automated reminders for vaccinations, farrowing, weaning, and other important pig operations'
                    },
                
                    {
                        'img_path': '/static_m/images/mar/mar_pig_ops.png?v=%s' % app_version,
                        'title': 'Traceability of Pig Operations',
                        'desc': 'Clear tracking who did the pig operation and when and what dosages given to pigs'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_fattening.png?v=%s' % app_version,
                        'title': 'Track and estimate Fatteners feed requirements',
                        'desc': 'Record every vaccine, medicine, health issue, history for each production cycle'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_feed_records.png?v=%s' % app_version,
                        'title': 'Record feeds consumption  per production batch',
                        'desc': 'Feed Balance and audit can be recorded anytime.'
                    },
                    
                    {
                        'img_path': '/static_m/images/mar/mar_report.png?v=%s' % app_version,
                        'title': 'Generate Status Report for your Farm',
                        'desc': 'Comprehensive reporting to know the status of your pig farm.'
                    }
                ]
            }
            
            
            # Mobile version
            template = env.get_template('home.html')
            
            
            # Get appropriate JS files based on environment
            js_app_text = []
            
            
            # These should have type= text/javascript
            js_lib  = []
            
        
            # These should have type= module
            js_app_modules = []
            
            
            s_translation = None
            if translation is not None:
                s_translation = json.dumps(translation)
            

                
            data    = { 'page_data':        page_data,
                        'js_lib':           js_lib,
                        'js_app_text':      js_app_text,
                        'js_app_modules':   js_app_modules,
                        'is_dev':           self.is_dev,
                        'translation':      s_translation
                    }
            
                    
            return template.render(data)
            


class AccPigOps(ViewBase):
    def render(self, page_data = None):
        
        template = env.get_template('acc_pig_ops.html')
        
        js_lib  = [ 'library/pqtouch.min.js', 
                    'library/pqselect.min.js',
                    'library/pqgrid.min-3.5.1.js']
                    
        # TODO minify and obfuscate js
        js_app  = [ 'models/model_00_master.js',
 
                    'models/account/model_acc_pig_ops.js',
                    
                    'pages/acc_pig_ops/add_acc_pig_ops_modal.js',
                    'pages/acc_pig_ops/update_acc_pig_ops_settings.js',
                    'pages/acc_pig_ops/page_acc_pig_ops.js']
        
        scripts = js_lib + js_app
        
        data    = { 'page_data': page_data,
                    'scripts' : scripts}
        
                
        return template.render(data)



class SowBoar(ViewBase):
    def render(self, page_data = None):
        
        template = env.get_template('sow_boar.html')
        
        js_lib  = [ 'library/pqtouch.min.js', 
                    'library/pqselect.min.js',
                    'library/pqgrid.min-3.5.1.js']
                    
        # TODO minify and obfuscate js
        js_app  = [ 'models/model_00_master.js',
 
                    'models/operations/model_farm_staff.js',
                    
                    'models/prod_details/model_notes.js',
                    'models/sow_boar/model_sow_boar.js',
                    'models/sow_boar/model_sow_production.js',
                    
                    'pages/production/common/tr_add_new_farm_staff.js',
                    
                    'pages/production/details/modal/add_modal_notes.js',
                    'pages/production/details/modal/add_modal_pig_dead.js',                   
                    
                    'pages/production/details/prod_notes.js',                    
                    'pages/production/details/prod_details.js',
                    
                    'pages/sow_boar/modal/add_modal_sow_boar.js',
                    'pages/sow_boar/page_sow_boar.js']
        
        scripts = js_lib + js_app
        
        data    = { 'page_data': page_data,
                    'scripts' : scripts}
        
                
        return template.render(data)



class PigProd(ViewBase):
    def render(self, page_data = None, is_mobile = 0):
        
        if is_mobile == 0:
            #Desktop version
            template = env.get_template('pig_production.html')
            
            js_lib  = [ 'library/pqtouch.min.js', 
                        'library/pqselect.min.js',
                        'library/pqgrid.min-3.5.1.js']
                        
            # TODO minify and obfuscate js
            js_app  = [ 'components/plus_minus_number_input.js',
                        'components/card_prod_pig_ops.js',
                        
                        'models/model_00_master.js',
                        
                        'models/common/model_with_address_and_contact.js',
                        
                        'models/operations/model_farm_staff.js',
                        'models/prod_details/model_notes.js',
                        'models/prod_details/model_pig_dead.js',
                        'models/prod_details/feed/model_feed_buy.js',
                        'models/prod_details/feed/model_feed_balance.js',
                        'models/production/model_pig_production.js',
                        
                        'models/sow_boar/model_sow_boar.js',
                        
                        'pages/production/common/tr_add_new_farm_staff.js',
                        
                        'pages/common/address_manager.js',
                        'pages/common/contact_details.js',
                        
                        'pages/common/tr_field_with_adrs_level_edit.js',
                        'pages/common/tr_field_with_adrs_level.js',
                        
                        
                        'pages/common/tr_add_new_item_with_adrs_level.js',
                        
                        'pages/production/details/modal/add_modal_notes.js',
                        
                        'pages/production/details/modal/tr_add_new_feed_brand.js',
                        'pages/production/details/modal/tr_add_new_feed_supplier.js',
                        'pages/production/details/modal/add_modal_feed_buy.js',
                        
                        'pages/production/details/modal/add_modal_feed_balance.js',
                        'pages/production/details/modal/add_modal_pig_dead.js',
                        
                        
                        'pages/production/details/prod_notes.js',
                        'pages/production/details/prod_pig_dead.js',
                        'pages/production/details/prod_feed_buy.js',
                        'pages/production/details/prod_feed_summary.js',
                        'pages/production/details/prod_details.js',
                        
                        'pages/production/prod_ops.js',
                        
                        'pages/production/gestating/tr_add_new_sow_boar.js',
                        'pages/production/gestating/tr_add_new_semen.js',
                        
                        'pages/production/gestating/gestating_add.js',
                        'pages/production/gestating/gestating_update_insem.js',
                        'pages/production/gestating/gestating_update_birth.js',
                        'pages/production/gestating/gestating_update_status.js',
                        'pages/production/gestating/prod_gestating.js',
                        
                        'pages/production/lactating/add_modal_eartag_piglet.js',
                        
                        'pages/production/prod_lactating.js',
                        'pages/production/page_pig_production.js']
            
            scripts = js_lib + js_app
            
            data    = { 'page_data': page_data,
                        'scripts' : scripts}
            
                    
            return template.render(data)

        
        
        # Mobile version
        template = env.get_template('pig_production_mob.html')
        
        # These should have type= text/javascript
        js_lib  = []
        
        
        # TODO minify and obfuscate js
        
        # These should have type= text/javascript
        js_app_text     = []
    
        # These should have type= module
        js_app_modules = [
            "/static_m/js/constants.js",
            "/static_m/js/utils.js",
            
            
            "/static_m/js/models/model_basic.js",
            "/static_m/js/models/model_acc_pig_ops.js",
            "/static_m/js/models/model_pig_production.js",
            
            
            "/static_m/js/pages/common/page_view_basic.js",
            "/static_m/js/pages/navigation/text_substitute_control.js",
            
            "/static_m/js/pages/acc_pig_ops/add_modal_acc_pig_ops.js",
            "/static_m/js/pages/acc_pig_ops/edit_modal_acc_pig_ops.js",
            "/static_m/js/pages/acc_pig_ops/page_acc_pig_ops.js",
            
            
            "/static_m/js/pages/sow_boar/page_sow_boar_list.js",
            "/static_m/js/pages/sow_boar/page_sow_boar_add_edit.js",
            
            
                
            
            "/static_m/js/pages/production/gesta_lacta/insem_data_select.js",
            "/static_m/js/pages/production/gesta_lacta/page_prod_gestating_add.js",
            
            "/static_m/js/pages/production/gesta_lacta/prod_entry_notes.js",
            "/static_m/js/pages/production/gesta_lacta/prod_entry_pig_ops.js",
            "/static_m/js/pages/production/gesta_lacta/prod_entry_insem.js",
            "/static_m/js/pages/production/gesta_lacta/prod_entry_birth.js",
            "/static_m/js/pages/production/gesta_lacta/page_prod_gestating_entry.js",
            
            
            
            "/static_m/js/pages/production/gesta_lacta/page_mob_gesta_lacta.js",
            
            
            "/static_m/js/pages/navigation/navigation.js"
        ]
            
        data    = { 'page_data':        page_data,
                    'js_lib':           js_lib,
                    'js_app_text':      js_app_text,
                    'js_app_modules':   js_app_modules}
        
                
        return template.render(data)
