# September 9, 2025
# Jack Wong

import os
import sys
import pprint

import pandas               as pd

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *



class FeedCalculator:
    def __init__(self, pig_farm_id):
        self.model          = model
        self.logger         = logger
        self.pig_farm_id    = pig_farm_id
        
        
    def estimate_consumption_by_date(self, date_s):
        
        pd_prod = self.model['feed_calc'].get_pig_prod_list(self.pig_farm_id)
        
        pd_prod['con_num_LAC']  = pd_prod['buy_num_LAC']    - pd_prod['bal_num_LAC']
        pd_prod['bal_kg_LAC']   = pd_prod['buy_kg_LAC']     - pd_prod['con_kg_LAC']
        
        
        pd_prod['con_num_BOS']  = pd_prod['buy_num_BOS']    - pd_prod['bal_num_BOS']
        pd_prod['bal_kg_BOS']   = pd_prod['buy_kg_BOS']     - pd_prod['con_kg_BOS']
        
        
        pd_prod['con_num_PRE']  = pd_prod['buy_num_PRE']    - pd_prod['bal_num_PRE']
        pd_prod['bal_kg_PRE']   = pd_prod['buy_kg_PRE']     - pd_prod['con_kg_PRE']
        pd_prod['con_kg_PRE_pp']= pd_prod['con_num_PRE']    / pd_prod['num_pigs']
        
        
        pd_prod['con_num_STR']  = pd_prod['buy_num_STR']    - pd_prod['bal_num_STR']
        pd_prod['bal_kg_STR']   = pd_prod['buy_kg_STR']     - pd_prod['con_kg_STR']
        pd_prod['con_kg_STR_pp']= pd_prod['con_num_STR']    / pd_prod['num_pigs']
        
        
        pd_prod['con_num_GRO']  = pd_prod['buy_num_GRO']    - pd_prod['bal_num_GRO']
        pd_prod['bal_kg_GRO']   = pd_prod['buy_kg_GRO']     - pd_prod['con_kg_GRO']
        pd_prod['con_kg_GRO_pp']= pd_prod['con_num_GRO']    / pd_prod['num_pigs']
        
        
        pd_prod['con_num_FIN']  = pd_prod['buy_num_FIN']    - pd_prod['bal_num_FIN']
        pd_prod['bal_kg_FIN']   = pd_prod['buy_kg_FIN']     - pd_prod['con_kg_FIN']
        pd_prod['con_kg_FIN_pp']= pd_prod['con_num_FIN']    / pd_prod['num_pigs']
        
        
        
        return pd_prod
        