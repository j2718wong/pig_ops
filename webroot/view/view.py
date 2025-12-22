__author__ = "Jack Wong j2718wong@gmail.com"
__date__ = "2025-10-01 10:00:00"


import sys
import os


sys.path.append(os.path.dirname(__file__))


from jinja2             import Environment, FileSystemLoader



# Set up the Jinja environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('templates'))


view_names = [              
            
            ('acc_pig_ops',         'AccPigOps'),
            ('sow_boar',            'SowBoar'),
            ('pig_prod',            'PigProd')
            
           
            
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

    
#
# Views
#


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
    def render(self, page_data = None):
        
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

