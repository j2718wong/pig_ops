__author__ = "Jack Wong, jack.wong@erg.com.hk, neoaspilet1@gmail.com"
__date__ = "$2015-02-09 10:00:00$"


import sys
import os


sys.path.append(os.path.dirname(__file__))


from jinja2             import Environment, FileSystemLoader



# Set up the Jinja environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('templates'))


view_names = [              
           
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


# TODO minify and obfuscate js

class PigProd(ViewBase):
    def render(self, page_data = None):
        
        template = env.get_template('pig_production.html')
        
        scripts = [ 'library/pqtouch.min.js', 
                    'library/pqselect.min.js',
                    'library/pqgrid.min-3.5.1.js',
                    
                    'components/plus_minus_number_input.js',
                    'components/card_prod_pig_ops.js',
                    'components/add_notes_modal.js',
                    'components/add_feed_buy_modal.js',
                    'components/add_feed_balance_modal.js',
                    'components/add_pig_dead_modal.js',
                    
                    'models/model_00_master.js',
                    'models/model_01_master.js',
                    
                    'models/notes/model_notes.js',
                    'models/model_pig_dead.js',
                    'models/feed/model_feed_buy.js',
                    'models/feed/model_feed_balance.js',
                    'models/production/model_pig_production.js',
                    
                    'pages/production/prod_notes.js',
                    'pages/production/prod_pig_dead.js',
                    'pages/production/prod_feed_buy.js',
                    'pages/production/prod_feed_balance.js',
                    'pages/production/prod_ops.js',
                    
                    'pages/production/prod_details.js',
                    'pages/production/prod_gestating.js',
                    'pages/production/prod_lactating.js',
                    'pages/production/page_pig_production.js']
        
        data    = { 'page_data': page_data,
                    'scripts' : scripts}
        
                
        return template.render(data)

