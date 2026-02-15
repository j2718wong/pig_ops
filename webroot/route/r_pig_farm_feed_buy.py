# February 2, 2026
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

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


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description



  

@app.post("/pf_feed_buy/add", tags=["Pig Farm"])
async def pig_farm_feed_buy_add(feed_buy_data: dm.DataPigFarmFeedBuy):
    uhid    = feed_buy_data.uhid
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_farm_hid        = feed_buy_data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    pig_farm_id = res[0]

    
    feed_supplier_hid        = feed_buy_data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    feed_supplier_id = res[0]
    
    
    
    
    
    feed_buy_data.user_id           = user_id
    feed_buy_data.pig_farm_id       = pig_farm_id
    feed_buy_data.feed_supplier_id  = feed_supplier_id
    
    res_add    =  model['pf_feed_buy'].add(feed_buy_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    # remove plain id
    cur_id      = res_add['pf_feed_buy']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_add['pf_feed_buy']['id']
    res_add['pf_feed_buy']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    
    
@app.post("/pf_feed_buy/update", tags=["Pig Farm"])
async def pig_farm_feed_buy_update(feed_buy_data: dm.DataPigFarmFeedBuy):
    uhid    = feed_buy_data.uhid
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pf_feed_buy_hid = feed_buy_data.pf_feed_buy_hid
    
    
    res = hashids_common.decrypt(pf_feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID'
            }
        }
    
    pf_feed_buy_id = res[0]
    
    
    feed_supplier_hid        = feed_buy_data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    feed_supplier_id = res[0]
    
    
    
    feed_buy_data.user_id   = user_id
    feed_buy_data.pf_feed_buy_id = pf_feed_buy_id
    feed_buy_data.feed_supplier_id  = feed_supplier_id
    
    res_update    =  model['pf_feed_buy'].update(feed_buy_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    cur_id      = res_update['pf_feed_buy']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_update['pf_feed_buy']['id']
    res_update['pf_feed_buy']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update
    
    
def replace_plain_ids_feed_item(cur_entry):
    cur_id  = cur_entry['feed_item']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_item']['id']
    cur_entry['feed_item']['hid']   = cur_hid
    
    
    cur_id  = cur_entry['feed_type']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_type']['id']
    cur_entry['feed_type']['hid']   = cur_hid
    
    
    cur_id  = cur_entry['feed_brand']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_brand']['id']
    cur_entry['feed_brand']['hid']   = cur_hid
    
    
    
@app.get("/pf_feed_buy/list", tags=["Pig Farm"])
async def pf_feed_buy_list(pfhid: str, page_number = 1):
    """
    Will get pig farm feed_buy list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid

        
    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        return result
        
    pig_farm_id = res[0]


    res = model['pf_feed_buy'].get_list(pig_farm_id, page_number)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pf_feed_buy']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pf_feed_buy']['id']
        cur_entry['pf_feed_buy']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['feed_supplier']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_supplier']['id']
        cur_entry['feed_supplier']['hid']   = cur_hid
        
        
        for cur_item in cur_entry['feed_items']:
            replace_plain_ids_feed_item(cur_item)
            
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
