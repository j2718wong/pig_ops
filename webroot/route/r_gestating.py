# August 17, 2025
# Jack Wong

import os
import sys
import json
import pprint

from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)



from r_utils                import get_location_address_names_and_replace_ids




@app.get("/account/gestating_data", tags=["Pig Production"])
async def account_gestating_data(pfhid:str = None):
    # Get the current logged in user;
    
    pig_farm_id = None
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            # Just proceed if it is invalid; will get default 
            # account farm_id if not given
            test = 1
            
            """
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
            """
        else:
            pig_farm_id = res[0]
            
    
    # temporary
    user_id = 1
   
    res_user = model['user'].get_user_info(user_id)
    if res_user == None:
        # TODO what to do in case no result
        print('Error 1')
        return None
        
        
    # Get user.account_id 
    account_id = res_user['user']['account_id']
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        print('Error 2')
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
        
    # Check if there is a farm_id list
    account_farm_ids = data_account['farm_ids']
    len_items = len(account_farm_ids)
    if len_items == 0:
        # TODO what to do in case no farm set
        print('Error 3')
        return None
        
    if pig_farm_id is not None:
        # This is given by user 
        
        if pig_farm_id not in account_farm_ids:
            # TODO what to do in case farm_id given is not in account list
            print('Error 4')
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = account_farm_ids[0]
        
    
    
    
    # Get pig_farm sow list
    list_sow_list = model['sow_boar'].get_list(pig_farm_id, 'F', 
        is_disposed = 0, inc_external = 0, is_production_ready = 1,
        inc_user_audit = 0, minimum_info = 1, order_by = 1)
    if list_sow_list == None:
        # TODO what to do in case no result
        print('Error 9')
        return None
    
    
    # Get pig_farm boar list
    list_boar_list = model['sow_boar'].get_list(pig_farm_id, 'M', 
        is_disposed = 0, inc_external = 1, is_production_ready = 1,
        inc_user_audit = 0, minimum_info = 1, order_by = 1)
    if list_boar_list == None:
        # TODO what to do in case no result
        print('Error 10')
        return None
    
    
    # Get semen_supplier list
    #list_semen_supplier = model['semen_supplier'].get_list(
    #    account_id = account_id, minimum_info = 0)
    
    list_semen_supplier = model['supplier'].get_list(
        account_id          = account_id, 
        is_semen_supplier   = 1,
        minimum_info        = 0)
    
    if list_semen_supplier == None:
        # TODO what to do in case no result
        print('Error 11')
        return None
        
    
    # Get farm_staff list
    list_staff = model['pig_farm_staff'].get_list(pig_farm_id)
    if list_staff == None:
        # TODO what to do in case no result
        print('Error 12')
        return None
        
    

    # Remove plain_ids and not useful data blocks
    
    
    
    
    for cur_entry in list_sow_list:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    
    for cur_entry in list_boar_list:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
       
    for cur_entry in list_semen_supplier:
        cur_id      = cur_entry['supplier']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['supplier']['id']
        cur_entry['supplier']['hid']   = cur_hid
        
        
    for cur_entry in list_staff:
        cur_id      = cur_entry['pig_farm_staff']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_farm_staff']['id']
        cur_entry['pig_farm_staff']['hid']   = cur_hid
        
        
        cur_id      = cur_entry['pig_farm_staff']['user_id']
        
        if cur_id > 0:
            cur_hid     = hashids_user.encrypt(cur_id)
            
            del cur_entry['pig_farm_staff']['user_id']
            cur_entry['pig_farm_staff']['user_hid']   = cur_hid
        else:
            cur_entry['pig_farm_staff']['user_hid']   = '';
        
    
    
    for cur_entry in list_feed_supplier:
        cur_id      = cur_entry['supplier']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['supplier']['id']
        cur_entry['supplier']['hid']   = cur_hid

        
        get_location_address_names_and_replace_ids(cur_entry)
    
    
    for cur_entry in list_semen_supplier:
        get_location_address_names_and_replace_ids(cur_entry)
    
    
    
    
    result = {
        'sow_list':                 list_sow_list,
        'boar_list':                list_boar_list,
        'semen_supplier_list':      list_semen_supplier,
        'staff_list':               list_staff
        
    }
    

    return result
    

