# September 28, 2025
# Jack Wong

import os
import sys


from datetime               import datetime, timedelta

from common_constants       import *


import requests
import json
import pprint


ADDRESS_SERVER = 'http://localhost:8081/'


class AddressManager:
    def __init__(self, logger):
        self.TAG        = 'AddressManager'
        self.logger     = logger
        
        
    def get_address_level_names(self, level_1_id, level_2_id, level_3_id=0):
    
        url = ADDRESS_SERVER  + 'address/level/names?'
        url += 'adrs_level_1_id=%s&' % level_1_id
        url += 'adrs_level_2_id=%s&' % level_2_id
        url += 'adrs_level_3_id=%s&' % level_3_id
        
        r = requests.get(url)
        
        
        if r.status_code != 200:
            s  = "get_address_level_names(); Error in requesting url: %s\n" % url
            s += "status_code = %s"  % r.status_code
            
            self.logger.append(tag = self.TAG, msg = s)
            
            return None
        
        
        res_text = str(r.text)
        res_json = json.loads(res_text)

        
        return res_json['data']

        
        

