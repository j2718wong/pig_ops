# November 27, 2025
# Jack Wong (zhaoshan99@gmail.com)


class JSMinifier:
    def __init__(self):
        test = 1


class Controller:
    
    def __init__(self, logger = None, model = None):
        self.TAG                = 'Model'
        
        self.is_prod_envi       = False
        
        self.use_minified_js    = 1
        
        self.logger             = logger
        
        self.model              = model
        
        
        self.view               = None
        
        
    def set_view(self, view):
        self.view = view
        
        
        
        
