# November 27, 2025
# Jack Wong (zhaoshan99@gmail.com)


class Controller:
    
    def __init__(self, logger = None, model = None):
        self.TAG                = 'Model'
        
        self.logger             = logger
        
        self.model              = model
        
        self.view               = None
        
        
    def set_view(self, view):
        self.view = view