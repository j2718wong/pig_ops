# August 10, 2025
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
                                    get_location_address_names_and_replace_ids)




  

@app.post("/pig_farm/add", tags=["Pig Farm"])
async def pig_farm_add(request: Request, data: dm.DataPigFarm):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_INVALID_NAME'
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    data.name      = name
    data.user_id   = user_id
    
    
    if data.country_id == 0:
        data.country_id = 1 # Default
    
    res_add    =  model['pig_farm'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain ids
    cur_id     = res_add['pig_farm']['id']
    cur_hid    = hashids_common.encrypt(cur_id)
    
    pig_farm_id     = cur_id
    pig_farm_hid    = cur_hid    
    
    del res_add['pig_farm']['id']
    res_add['pig_farm']['hid'] = cur_hid

    result_num      = res_add['result']['num']
    
    if result_num == 0:
        data = {
           'pig_farm_id':   pig_farm_id,
           'hashid':        pig_farm_hid
        }
        res_update = model['pig_farm'].update_hashid(data)
    
    
    return res_add
    
    
@app.post("/pig_farm/update", tags=["Pig Farm"])
async def pig_farm_update(request: Request, data: dm.DataPigFarm):
    """
    The pig farm update vary a little bit from normal add/update returns;
    It will return the pig_farm object so no need to request again for 
    the pig_farm entry.
    """    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_INVALID_NAME'
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    
    user_id = res[0]
    
    
    pig_farm_hid = data.pig_farm_hid
    
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID'
            }
        }
    
    
    pig_farm_id = res[0]
    
    
    level_1_id  = 0
    level_2_id  = 0
    level_3_id  = 0
    
    
    level_1_hid = data.level_1_hid
    res = hashids_common.decrypt(level_1_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_INVALID_ADDRESS_LEVEL_1,
                'code': 'ERROR_INVALID_ADDRESS_LEVEL_1'
            }
        }
        
    level_1_id = res[0]
    
    
    level_2_hid = data.level_2_hid
    res = hashids_common.decrypt(level_2_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_INVALID_ADDRESS_LEVEL_2,
                'code': 'ERROR_INVALID_ADDRESS_LEVEL_2'
            }
        }
    
    level_2_id = res[0]
    
    
    level_3_hid = data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_INVALID_ADDRESS_LEVEL_3'
                }
            }
        
        level_3_id = res[0]
    
    
    
    
    data.name          = name
    data.user_id       = user_id
    data.pig_farm_id   = pig_farm_id
    data.level_1_id    = level_1_id
    data.level_2_id    = level_2_id
    data.level_3_id    = level_3_id
    
    
    
    res_update    =  model['pig_farm'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    if res_update['result']['num'] != 0:
        
        # remove plain id
        del res_update['pig_farm']['id']
        res_update['pig_farm']['hid'] = pig_farm_hid
            
        return res_update


    # Request pig_farm entry
    id_list = [pig_farm_id]
    res_list = model['pig_farm'].get_list(id_list = id_list)
    
    if res_list is None or len(res_list) != 1:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }

    
    res = res_list[0]
    
    # Replace plain ids
    cur_id     = res['pig_farm']['id']
    cur_hid    = hashids_common.encrypt(cur_id)
    
    del res['pig_farm']['id']
    res['pig_farm']['hid'] = cur_hid

    
    get_location_address_names_and_replace_ids(res)
    
    
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

@app.get("/pig_farm/list", tags=["Pig Farm"])
async def pig_farm_list(request: Request, ahid: str):
    """
    Will get pig farm list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        

    res                 = model['pig_farm'].get_list(account_id)

    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    for cur_entry in res:
        location_address    = cur_entry['location']['address']
        level_1_id          = location_address['level_1']['id']
        level_2_id          = location_address['level_2']['id']
        level_3_id          = location_address['level_3']['id']
        
        
        # Get location address names from another server
        res_address = model_la['address_level'].get_address_level_names(level_1_id, 
            level_2_id, level_3_id)
        
        if res_address is not None:
            location_address['level_1']['name'] = res_address['level_1_name']
            location_address['level_2']['name'] = res_address['level_2_name']
            location_address['level_3']['name'] = res_address['level_3_name']
            
            
        # replace plain_id 
        cur_id      = level_1_id
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['location']['address']['level_1']['id']
        cur_entry['location']['address']['level_1']['hid'] = cur_hid
        
        
        cur_id      = level_2_id
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['location']['address']['level_2']['id']
        cur_entry['location']['address']['level_2']['hid'] = cur_hid
        
        
        cur_id      = level_3_id
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['location']['address']['level_3']['id']
        cur_entry['location']['address']['level_3']['hid'] = cur_hid
        
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    


@app.get("/pig_farm/data_ver_num", tags=["Pig Farm"])
async def data_ver_num(pfid: str):
    """
    Will get pig farm data_ver_num.
    
    Parameters
    ----------
    
    pfid:str
        pig farm hashid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pfid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    pig_farm_id = res[0]
        

    res                 = model['pig_farm'].get_data_ver_num(pig_farm_id)

    
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
    


