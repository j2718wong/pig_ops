# February 14, 2026
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



   
@app.post("/pig_prod_feed/add", tags=["Production Details"])
async def pig_prod_feed_add(pig_prod_feed_data: dm.DataPigProdFeed):
    uhid    = pig_prod_feed_data.uhid
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    
    pig_prod_hid    = pig_prod_feed_data.pig_prod_hid

    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    pig_farm_feed_buy_hid    = pig_prod_feed_data.pig_farm_feed_buy_hid
    
    res = hashids_common.decrypt(pig_farm_feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_PF_FEED_BUY_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_PF_FEED_BUY_HASHID'
            }
        }
    
    pig_farm_feed_buy_id = res[0]
    
   

   
    pig_prod_feed_data.user_id              = user_id
    pig_prod_feed_data.pig_prod_id          = pig_prod_id
    pig_prod_feed_data.pig_farm_feed_buy_id = pig_farm_feed_buy_id
    
    res_add    =  model['pig_prod_feed'].add(pig_prod_feed_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    pig_prod_feed_id    = res_add['pig_prod_feed']['id']
    pig_prod_feed_hid   = hashids_common.encrypt(pig_prod_feed_id)
    
    # remove plain id
    del res_add['pig_prod_feed']['id']
    res_add['pig_prod_feed']['hid'] = pig_prod_feed_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    

@app.post("/pig_prod_feed/update", tags=["Production Details"])
async def pig_prod_feed_update(pig_prod_feed_data: dm.DataPigProdFeed):
    uhid    = pig_prod_feed_data.uhid

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_feed_hid = pig_prod_feed_data.pig_prod_feed_hid
    
    res = hashids_common.decrypt(pig_prod_feed_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_HASHID'
            }
        }
    
    
    pig_prod_feed_id = res[0]
    
    
    pig_prod_feed_data.user_id   = user_id
    pig_prod_feed_data.pig_prod_feed_id = pig_prod_feed_id
    
    res_update    =  model['prod_feed'].update(pig_prod_feed_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_feed']['id']
    res_update['pig_prod_feed']['hid'] = pig_prod_feed_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    
    return res_update
    

@app.get("/pig_prod_feed/delete", tags=["Production Details"])
async def pig_prod_feed_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_HASHID'
            }
        }
    
    pig_prod_feed_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_prod_feed_id':     pig_prod_feed_id
    }
    
    
    res_delete    =  model['pig_prod_feed'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_prod_feed']['id']
    res_delete['pig_prod_feed']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)
    
    
    return res_delete
    
    
def get_data_pig_prod_feed(pig_prod_id, sow_boar_id, prod_group_id, 
        inc_deleted, inc_user_audit):
            
    res = model['prod_feed'].get_list(pig_prod_id, sow_boar_id, prod_group_id, 
        inc_deleted, inc_user_audit)
    
    if res is None:
        return None
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['prod_feed']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['prod_feed']['id']
        cur_entry['prod_feed']['hid']   = cur_hid

        
        if 'pig_medvac' in cur_entry:
            cur_id  = cur_entry['pig_medvac']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['id']
            cur_entry['pig_medvac']['hid']   = cur_hid
    
    
    return res
    
    
    
@app.get("/pig_prod_feed/list", tags=["Production Details"])
async def pig_prod_feed_list(pig_prod_hid: str = None, sow_boar_hid: str = None,
    prod_group_hid = None, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig_prod_feed list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod_hid hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    pig_prod_id     = 0
    sow_boar_id     = 0
    prod_group_id   = 0
    
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID'
                }
            }
            
        pig_prod_id = res[0]
        
        
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_FEED_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_FEED_INVALID_SOW_BOAR_HASHID'
                }
            }
        
        sow_boar_id = res[0]
    
    
    if prod_group_hid is not None:
        res = hashids_common.decrypt(prod_group_id)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_FEED_INVALID_PROD_GROUP_HASHID,
                    'code': 'ERROR_PIG_PROD_FEED_INVALID_PROD_GROUP_HASHID'
                }
            }
        
        prod_group_id = res[0]
    
    
        
    res = get_data_pig_prod_feed(pig_prod_id, sow_boar_id, prod_group_id, 
        inc_deleted, inc_user_audit)
    
    
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
    
    

    
