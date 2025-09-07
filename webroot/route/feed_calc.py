
class FeedCalculator:
    def __init__(self, model, logger, pig_farm_id):
        self.model          = model
        self.logger         = logger
        self.pig_farm_id    = pig_farm_id
        
        
    def estimate_consumption_by_date(self, date_s):
        
        