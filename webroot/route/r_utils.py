# December 17, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *



def get_location_address_names_and_replace_ids(cur_entry):
    # Get location address names from a different database
    location_address = cur_entry['location']['address']
        
    level_1_id = location_address['level_1']['id']
    level_2_id = location_address['level_2']['id']
    level_3_id = location_address['level_3']['id']
    
    if level_3_id is None:
        level_3_id = 0
    
    address_names = model_la['address_level'].get_address_level_names(
        address_level_1_id = level_1_id, 
        address_level_2_id = level_2_id,
        address_level_3_id = level_3_id
    )
    
    if address_names is not None:
        location_address['level_1']['name'] = address_names['level_1_name']
        location_address['level_2']['name'] = address_names['level_2_name']
        location_address['level_3']['name'] = address_names['level_3_name']
        
    
    
    
    cur_id      = cur_entry['location']['address']['level_1']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del cur_entry['location']['address']['level_1']['id']
    cur_entry['location']['address']['level_1']['hid']   = cur_hid

    
    cur_id      = cur_entry['location']['address']['level_2']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del cur_entry['location']['address']['level_2']['id']
    cur_entry['location']['address']['level_2']['hid']   = cur_hid


    cur_id      = cur_entry['location']['address']['level_3']['id']
    if cur_id is not None and cur_id > 0:
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['location']['address']['level_3']['id']
        cur_entry['location']['address']['level_3']['hid']   = cur_hid


