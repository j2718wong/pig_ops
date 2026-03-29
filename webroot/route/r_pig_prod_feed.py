# February 14, 2026
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse


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
from r_pig_farm_feed_buy    import replace_plain_ids_feed_item


   
@app.post("/pig_prod_feed/add", tags=["Production Details"])
async def pig_prod_feed_add(request: Request, data: dm.DataPigProdFeed):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    
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
    
    
    
    
    pig_prod_hid    = data.pig_prod_hid

    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    pig_farm_feed_buy_hid    = data.pig_farm_feed_buy_hid
    
    res = hashids_common.decrypt(pig_farm_feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_PF_FEED_BUY_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_PF_FEED_BUY_HASHID'
            }
        }
    
    pig_farm_feed_buy_id = res[0]
    
   

   
    data.user_id              = user_id
    data.pig_prod_id          = pig_prod_id
    data.pig_farm_feed_buy_id = pig_farm_feed_buy_id
    
    res_add    =  model['pig_prod_feed'].add(data)
    
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
async def pig_prod_feed_update(request: Request, data: dm.DataPigProdFeed):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_feed_hid = data.pig_prod_feed_hid
    
    res = hashids_common.decrypt(pig_prod_feed_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_HASHID'
            }
        }
    
    
    pig_prod_feed_id = res[0]
    
    
    data.user_id   = user_id
    data.pig_prod_feed_id = pig_prod_feed_id
    
    
    if data.num_gesta is None:
        data.num_gesta = 0
    
    if data.num_lacta is None:
        data.num_lacta = 0
    
    if data.num_booster is None:
        data.num_booster = 0
    
    if data.num_prestarter is None:
        data.num_prestarter = 0
    
    if data.num_starter is None:
        data.num_starter = 0
    
    if data.num_grower is None:
        data.num_grower = 0
    
    if data.num_finisher is None:
        data.num_finisher = 0
    
    
    res_update    =  model['pig_prod_feed'].update(data)
    
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
async def pig_prod_feed_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
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
    
    
def get_data_pig_prod_feed(pig_prod_id):
            
    res = model['pig_prod_feed'].get_list(pig_prod_id)
    
    if res is None:
        return None
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pig_prod_feed']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_prod_feed']['id']
        cur_entry['pig_prod_feed']['hid']   = cur_hid
        
        
        
        cur_id  = cur_entry['pig_prod_feed']['pf_feed_buy_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_prod_feed']['pf_feed_buy_id']
        cur_entry['pig_prod_feed']['pf_feed_buy_hid']   = cur_hid
        
        
        
        
        cur_id  = cur_entry['feed_supplier']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_supplier']['id']
        cur_entry['feed_supplier']['hid']   = cur_hid
        
        
        
        for cur_item in cur_entry['feed_items']:
            replace_plain_ids_feed_item(cur_item)
    
    
    return res
    
    
    
@app.get("/pig_prod_feed/list", tags=["Production Details"])
async def pig_prod_feed_list(request: Request, pig_prod_hid: str = None):
    """
    Will get pig_prod_feed list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod_hid hashid

   
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    pig_prod_id     = 0

    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_FEED_INVALID_PIG_PROD_HASHID'
            }
        }
        
    pig_prod_id = res[0]
        
        
        
    res = get_data_pig_prod_feed(pig_prod_id)
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    

    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
