__author__ = "Jack Wong j2718wong@gmail.com"
__date__ = "2025-10-01 10:00:00"


import sys
import os
import json
import pprint


from common_fast_api        import dir_static

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


# Include the directory one level up from this script
sys.path.append(os.path.join(module_directory, '..')) 



from jinja2             import Environment, FileSystemLoader

from common_fast_api    import dir_static, dir_static_m


# Set up the Jinja environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('templates'))


view_names = [
            ('signup',              'SignUp'),
            
            ('root',                'Root'),
            
            ('acc_pig_ops',         'AccPigOps'),
            ('sow_boar',            'SowBoar'),
            ('pig_prod',            'PigProd')
            
           
            
        ]


MODULES_SIGNUP =[
    "pages/account_management/page_user_signup_or_login.js"
]


MODULES_ROOT = [
    "pages/navigation/navigation.js"
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
    
    

class SignUp(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('signup.html')
        
        # Read manifest file to get current bundle filenames
        manifest = self.get_manifest()
        
        pprint.pprint(manifest)
        
    
        data    = {}
        
        # These should have type= text/javascript
        js_app_text     = [
            f'/static/js/{manifest.get("login", "bundle.min.js")}'
        ]
        
        # These should have type= module
        js_app_modules = MODULES_SIGNUP
            
        data    = { 'page_data':        page_data,
                    'js_lib':           [],
                    'js_app_text':      js_app_text,
                    'js_app_modules':   []}
        
                
        return template.render(data)
    
#
# Views
#

"""
2026-01-03
1.) The is_mobile parameter in the view pages below is a temporary solution
to serve static files for mobile web page.

2.) As of this writing there are  two  separate locations for 
    - initial development web focused; mostly data is presented as tables.
    
    - development shift to Mobile first, desktop next
    
3.) The desktop version should work regardless of status of the mobile version.
    
    
    
"""

class Root(ViewBase):
    def render(self, page_data = None):
        # Mobile version
        template = env.get_template('index_mob.html')
        
        # Read manifest file to get current bundle filenames
        manifest = self.get_manifest()
        
        
        
        # These should have type= text/javascript
        js_lib  = []
        
        
        # These should have type= text/javascript
        js_app_text     = [
            f'/static/js/{manifest.get("core", "bundle.core.min.js")}'
        ]
    
        # These should have type= module
        js_app_modules = []
            
        data    = { 'page_data':        page_data,
                    'js_lib':           js_lib,
                    'js_app_text':      js_app_text,
                    'js_app_modules':   js_app_modules}
        
                
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
