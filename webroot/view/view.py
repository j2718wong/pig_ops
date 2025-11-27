__author__ = "Jack Wong, jack.wong@erg.com.hk, neoaspilet1@gmail.com"
__date__ = "$2015-02-09 10:00:00$"


from mako.template import Template

from view_base          import ViewBase
from render             import RenderNode, TopRenderNode



view_names = [              
            ('home',                'HomePage'),
            ('login',               'Login'),
            ('my_account',          'MyAccount'),
            ('under_construction',  'UnderConstruction'),
            ('error_404',           'Error404'),
            ('no_entry',            'NoEntry'),
            
            ('pig_prod',            'PigProd'),
           
            
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


    
#
# Views
#
class HomePage(ViewBase):
    def render(self, page_data = None):
        template = 'templates/public/home.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(text = text, 
                scripts = ['name_lookup.js', 
                            'models/model_00_master.js',
                            'models/model_01_master.js',
                            'models/model_parameter.js',
                            'models/device/model_device_event_log.js',
                            'pages/home_page.js',
                            'jquery/Chart.min.js'], 
                css = ['font-awesome.min.css',
                        'pure-min.css'])
        return top_node.render(controller = self.controller)


class Login(ViewBase):
    def render(self):
        template = 'templates/public/login.html'
        text = Template(filename = template).render(controller = self.controller)
        top_node = TopRenderNode(
                text = text, 
                scripts = [], 
                css =[])
        return top_node.render(controller = self.controller)


class MyAccount(ViewBase):
    def render(self, page_data = None):
        template = 'templates/sys_admin/my_account.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text, 
                scripts = ['others/webtoolkit.sha256.js', 
                        'user_account.js'], 
                css =[])
        return top_node.render(controller = self.controller)


class UnderConstruction(ViewBase):
    def render(self, page_data = None):
        template = 'templates/public/under_construction.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = [], 
                css =[])
        return top_node.render(controller = self.controller)


class Error404(ViewBase):
    def render(self, page_data = None):
        template = 'templates/public/page_error_404.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = [], 
                css =[])
        return top_node.render(controller = self.controller)



class NoEntry(ViewBase):
    def render(self, page_data = None):
        template = 'templates/public/no_entry.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = [], 
                css =[])
        return top_node.render(controller = self.controller)
    
class Bus(ViewBase):
    def render(self, page_data = None):
        template = 'templates/bus/bus_list.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = ['name_lookup.js', 
                        'models/model_00_master.js',
                        'models/model_01_master.js',
                        'models/bus/model_bus_list.js', 
                        'pages/bus/bus_list.js'], 
                css =[])
        return top_node.render(controller = self.controller)


class BusDevice(ViewBase):
    def render(self, page_data = None):
        template = 'templates/bus/bus_device.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = ['name_lookup.js', 
                        'models/model_00_master.js',
                        'models/model_01_master.js',
                        'models/device/model_bus_device.js', 
                        'pages/bus/bus_devices.js'], 
                css =[])
        return top_node.render(controller = self.controller)


class BusRouteList(ViewBase):
    def render(self, page_data = None):
        template = 'templates/bus/route_list.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
                scripts = ['name_lookup.js', 
                        'models/model_00_master.js',
                        'models/model_01_master.js',
                        'models/model_parameter.js',
                        'models/bus/model_bus_stop.js',
                        'models/bus/model_route_entry.js', 
                        'models/bus/model_route_translation.js',
                        'models/bus/model_route_other_sp.js',
                        'pages/bus/bus_routes.js'], 
                css =[])
        return top_node.render(controller = self.controller)





# TODO minify and obfuscate js

class PigProd(ViewBase):
    def render(self, page_data = None):
        template = 'templates/pig_prod/pig_prod.html'
        text = Template(filename = template).render(
                controller = self.controller, page_data = page_data)
        top_node = TopRenderNode(
                text = text,
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
                            'pages/production/page_pig_production.js'
                           ], 
                css =[])
        return top_node.render(controller = self.controller)

