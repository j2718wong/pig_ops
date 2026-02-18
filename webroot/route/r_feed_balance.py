# August 29, 2025
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


   
@app.post("/feed_balance/add", tags=["Production Details"])
async def feed_balance_add(feed_balance_data: dm.DataProdFeedBal):
    uhid    = feed_balance_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BALANCE_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BALANCE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_prod_hid        = feed_balance_data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = feed_balance_data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_group_hid = res[0]
    

    
    feed_balance_data.user_id          = user_id
    feed_balance_data.pig_prod_id      = pig_prod_id
    feed_balance_data.pig_prod_group_id= pig_prod_group_id
    
    res_add    =  model['feed_balance'].add(feed_balance_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    feed_balance_id    = res_add['feed_balance']['id']
    feed_balance_hid   = hashids_common.encrypt(feed_balance_id)
    
    # remove plain id
    del res_add['feed_balance']['id']
    res_add['feed_balance']['hid'] = feed_balance_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
    return res_add
    

@app.post("/feed_balance/update", tags=["Production Details"])
async def feed_balance_update(feed_balance_data: dm.DataProdFeedBal):
    uhid    = feed_balance_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BALANCE_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BALANCE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    feed_balance_hid    = feed_balance_data.feed_balance_hid
    
    res = hashids_common.decrypt(feed_balance_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BALANCE_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_FEED_BALANCE_INVALID_FEED_BRAND_HASHID'
            }
        }
    
    feed_balance_id = res[0]
    
    
    feed_balance_data.user_id           = user_id
    feed_balance_data.feed_balance_id   = feed_balance_id
   
    
    res_update    =  model['feed_balance'].update(feed_balance_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['feed_balance']['id']
    res_update['feed_balance']['hid'] = feed_balance_hid
    
        
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
        
    return res_update


def get_data_feed_balance(pig_prod_id = 0, inc_user_audit:int = 0): 
    res = model['feed_balance'].get_list(pig_prod_id = pig_prod_id, 
            inc_user_audit = inc_user_audit)
    
    if res is None:
        return None
        
    # Replace plain id
    for cur_entry in res:
        cur_id    = cur_entry['feed_balance']['id']
        cur_hid   = hashids_common.encrypt(cur_id)
        
        # remove plain id
        del cur_entry['feed_balance']['id']
        cur_entry['feed_balance']['hid'] = cur_hid    
    
    return res
    
        
    
@app.get("/feed_balance/list", tags=["Production Details"])
async def feed_balance_list(pig_prod_hid: str, inc_user_audit:int = 0):
    """
    Will get feed_balance list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod hashid

    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID'
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = get_data_feed_balance(pig_prod_id = pig_prod_id, 
            inc_user_audit = inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    
