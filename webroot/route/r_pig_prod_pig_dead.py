# August 23, 2025
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



   
@app.post("/prod_pig_dead/add", tags=["Production Details"])
async def prod_pig_dead_add(request: Request, data: dm.DataPigProdDeadPig):
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
                'num':  ERROR_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_USER_HASHID'
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
                    'num':  ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_dead_type_hid   = data.pig_dead_type_hid
    pig_dead_type_id    = 0
    
    res = hashids_common.decrypt(pig_dead_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_PIG_DEAD_TYPE_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_PIG_DEAD_TYPE_HASHID'
            }
        }
    
    pig_dead_type_id = res[0]
    
    
    data.user_id          = user_id
    data.pig_prod_id      = pig_prod_id
    data.pig_dead_type_id = pig_dead_type_id
    
    res_add    =  model['prod_pig_dead'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    prod_pig_dead_id    = res_add['prod_pig_dead']['id']
    prod_pig_dead_hid   = hashids_common.encrypt(prod_pig_dead_id)
    
    # remove plain id
    del res_add['prod_pig_dead']['id']
    res_add['prod_pig_dead']['hid'] = prod_pig_dead_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
    return res_add
    

@app.post("/prod_pig_dead/update", tags=["Production Details"])
async def prod_pig_dead_update(request: Request, data: dm.DataPigProdDeadPig):
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
                'num':  ERROR_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    prod_pig_dead_hid = data.prod_pig_dead_hid
    
    res = hashids_common.decrypt(prod_pig_dead_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_HASHID'
            }
        }
    
    
    prod_pig_dead_id = res[0]
    
    
    data.user_id   = user_id
    data.prod_pig_dead_id = prod_pig_dead_id
    
    res_update    =  model['prod_pig_dead'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['prod_pig_dead']['id']
    res_update['prod_pig_dead']['hid'] = prod_pig_dead_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    
  
@app.get("/prod_pig_dead/list", tags=["Production Details"])
async def prod_pig_dead_list(request: Request, pfhid: str = None, 
        pig_prod_hid: str =None):
    """
    Will get prod_pig_dead list.
    
    Parameters
    ----------
    pig_farm_hid : str
        if this is given the return is count by pig_prod_id;
        
    dead_at_stage : int
        this is used only if pig_farm_hid is given;
        if == 1, will return dead pigs at PRODUCTION_STATUS_ID_LACTATING
        else: will return dead pigs at PRODUCTION_STATUS_ID_WEANING, PRODUCTION_STATUS_ID_GROWING
    
    pig_prod_hid:str
        pir_prod hashid

    
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    pig_farm_id = 0
    pig_prod_id = 0
    
    
    if pfhid is not None:
    
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_DEAD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_DEAD_INVALID_PIG_FARM_HASHID'
                }
            }
        
        pig_farm_id = res[0]
    
    
    
    if pig_prod_hid is not None:
    
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_id = res[0]
        
        
        
    if pig_farm_id == 0 and pig_prod_id == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_NO_VALID_KEY,
                'code': 'ERROR_PIG_DEAD_NO_VALID_KEY'
            }
        }

        
        
        
    res = model['prod_pig_dead'].get_list(
         pig_farm_id = pig_farm_id, pig_prod_id = pig_prod_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    if pig_farm_id > 0:
        for cur_entry in res:
            cur_id  = cur_entry['pig_dead']['id']
            cur_hid = hashids_common.encrypt(cur_id)
        
            del cur_entry['pig_dead']['id']
            cur_entry['pig_dead']['hid']   = cur_hid
            
            replace_plain_ids_pig_production(cur_entry['production'])
            
        
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
