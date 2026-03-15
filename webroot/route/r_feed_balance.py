# August 29, 2025
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
from r_utils                import (remove_database_null_description,
                                    replace_plain_ids_pig_production)


   
@app.post("/feed_balance/add", tags=["Production Details"])
async def feed_balance_add(request: Request, data: dm.DataFeedBalance):
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
    
    
    
    pig_farm_hid        = data.pig_farm_hid
    pig_farm_id         = 0
    
    if pig_farm_hid is not None:
        res = hashids_common.decrypt(pig_farm_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID'
                }
            }
        
        pig_farm_id = res[0]
    
    
    
    pig_prod_hid        = data.pig_prod_hid
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
        
    
    pig_prod_group_hid  = data.pig_prod_group_hid
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
    

    
    data.user_id          = user_id
    data.pig_prod_id      = pig_prod_id
    data.pig_prod_group_id= pig_prod_group_id
    
    res_add    =  model['feed_balance'].add(data)
    
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
async def feed_balance_update(request: Request, data: dm.DataFeedBalance):
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
    
    
    
    pig_prod_hid        = data.pig_prod_hid
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
    
    
    data.user_id           = user_id
    data.pig_prod_id       = pig_prod_id
   
    
    res_update    =  model['feed_balance'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    cur_id  = res_update['feed_balance']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    
    # remove plain id
    del res_update['feed_balance']['id']
    res_update['feed_balance']['hid'] = cur_hid
    
        
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
        
    return res_update



@app.post("/feed_balance_all/add", tags=["Production Details"])
async def feed_balance_all_add(request: Request):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    data = None
    
    try:
        # Parse JSON data from request body
        data = await request.json()
    except:
        data = None
        
    
    
    date_balance = data.get('date_balance')
    entries = data.get('entries', [])
    
    # Process the entries
    for entry in entries:
        if 'pig_prod_hid' in entry:
            pig_prod_hid = entry['pig_prod_hid']
            feed_balance = entry['feed_balance']
            
            pig_prod_id  = 0
    
            res = hashids_common.decrypt(pig_prod_hid)
            if len(res) == 0:
                return {
                    'result':{
                        'num':  ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID,
                        'code': 'ERROR_FEED_BALANCE_INVALID_PIG_PROD_HASHID'
                    }
                }
            
            pig_prod_id = res[0]
            
            
            # Map the 7-element array to named fields
            gesta       = feed_balance[0]
            lacta       = feed_balance[1]
            booster     = feed_balance[2]
            prestarter  = feed_balance[3]
            starter     = feed_balance[4]
            grower      = feed_balance[5]
            finisher    = feed_balance[6]
            
            
            cur_data = dm.DataFeedBalance(
                pig_prod_id     = pig_prod_id,
                date_balance    = date_balance,
                
                num_gesta       = gesta,     
                num_lacta       = lacta,     
                num_booster     = booster,   
                num_prestarter  = prestarter,
                num_starter     = starter,   
                num_grower      = grower,    
                num_finisher    = finisher  
            )
            
            
            res_add    =  model['feed_balance'].add(cur_data)
    
            if res_add is None:
                return {
                    'result':{
                        'num':  ERROR_DATABASE_ERROR,
                        'code': 'ERROR_DATABASE_ERROR'
                    }
                }
            
            
        elif 'pig_farm_hid' in entry:
            pig_farm_hid = entry['pig_farm_hid']
            feed_balance = entry

            pig_farm_id  = 0
    
            res = hashids_common.decrypt(pig_farm_hid)
            if len(res) == 0:
                return {
                    'result':{
                        'num':  ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID,
                        'code': 'ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID'
                    }
                }
            
            pig_farm_id = res[0]
            
            
            # Map the 7-element array to named fields
            gesta       = feed_balance[0]
            lacta       = feed_balance[1]
            booster     = feed_balance[2]
            prestarter  = feed_balance[3]
            starter     = feed_balance[4]
            grower      = feed_balance[5]
            finisher    = feed_balance[6]
            
            
            cur_data = dm.DataFeedBalance(
                pig_farm_id     = pig_farm_id,
                date_balance    = date_balance,
                
                num_gesta       = gesta,     
                num_lacta       = lacta,     
                num_booster     = booster,   
                num_prestarter  = prestarter,
                num_starter     = starter,   
                num_grower      = grower,    
                num_finisher    = finisher  
            )
            
            
            res_add    =  model['feed_balance'].add(cur_data)
    
            if res_add is None:
                return {
                    'result':{
                        'num':  ERROR_DATABASE_ERROR,
                        'code': 'ERROR_DATABASE_ERROR'
                    }
                }


    return {
        'result':{
            'num':  ERROR_DATABASE_ERROR,
            'code': 'ERROR_DATABASE_ERROR'
        }
    }
            






def get_data_feed_balance(pig_prod_id = 0, pig_farm_id = 0, 
        date_since = None, inc_user_audit:int = 0): 
    """
    This will return two different structures based on given input
    pig_prod_id  or pig_farm_id. 
    """
    
    res = model['feed_balance'].get_list(
            pig_prod_id     = pig_prod_id, 
            pig_farm_id     = pig_farm_id,
            date_since      = date_since,
            inc_user_audit  = inc_user_audit)
            
    
    if res is None:
        return None
        
        
    if pig_prod_id > 0:
        # Replace plain id
        for cur_entry in res:
            cur_id    = cur_entry['feed_balance']['id']
            cur_hid   = hashids_common.encrypt(cur_id)
            
            # remove plain id
            del cur_entry['feed_balance']['id']
            cur_entry['feed_balance']['hid'] = cur_hid    
        
        return res
    
    
    if pig_farm_id > 0:
        # Replace plain id
        for cur_entry in res:
            for cur_balance in cur_entry['feed_balance']:
                cur_id    = cur_balance['id']
                cur_hid   = hashids_common.encrypt(cur_id)
                
                # remove plain id
                del cur_balance['id']
                cur_balance['hid'] = cur_hid    
                
                
                if 'pig_prod' in cur_balance:
                    pig_prod = cur_balance['pig_prod']
                    replace_plain_ids_pig_production(pig_prod)
                
        return res
    
    return None
    
    
@app.get("/feed_balance/list", tags=["Production Details"])
async def feed_balance_list(request: Request,  pig_prod_hid: str = None, pig_farm_hid = None, 
    date_since = None, inc_user_audit:int = 0):
    """
    Will get feed_balance list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod hashid
        
        
    pig_farm_hid :str    
        pig_farm hashid
    
    date_since: str
        date string in YYYY-MM-DD format
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    pig_prod_id = 0
    
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
    
    
    pig_farm_id = 0
    
    if pig_farm_hid is not None:
    
        res = hashids_common.decrypt(pig_farm_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_FEED_BALANCE_INVALID_PIG_FARM_HASHID'
                }
            }
        
        pig_farm_id = res[0]
    
    
        
    res = get_data_feed_balance(pig_prod_id = pig_prod_id, 
            pig_farm_id = pig_farm_id, date_since = date_since, 
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
    
    

    
