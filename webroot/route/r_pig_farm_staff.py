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
from r_utils                import remove_database_null_description

   
   
@app.post("/pig_farm_staff/add", tags=["Pig Farm"])
async def pig_farm_staff(request: Request, data: dm.DataPigFarmStaff):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if data.set_user_as_staff == 0:
        if name is None or len(name) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_FARM_STAFF_INVALID_NAME,
                    'code': 'ERROR_PIG_FARM_STAFF_INVALID_NAME'
                }
            }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_farm_hid = data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_PIG_FARM_HASHID'
            }
        }
       
    pig_farm_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    data.name            = name
    data.user_id         = user_id
    data.pig_farm_id     = pig_farm_id
  
    res_add    =  model['pig_farm_staff'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    pig_farm_staff_id    = res_add['pig_farm_staff']['id']
    pig_farm_staff_hid   = hashids_common.encrypt(pig_farm_staff_id)
    
    # remove plain id
    del res_add['pig_farm_staff']['id']
    res_add['pig_farm_staff']['hid'] = pig_farm_staff_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
    
    return res_add
    

@app.post("/pig_farm_staff/update", tags=["Pig Farm"])
async def pig_farm_staff_update(request: Request, data: dm.DataPigFarmStaff):
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
                'num':  ERROR_PIG_FARM_STAFF_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_NAME'
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']

    
    
    pig_farm_hid = data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID'
            }
        }
        
    pig_farm_id = res[0]
    
    
    pig_farm_staff_hid = data.pig_farm_staff_hid
    
    res = hashids_common.decrypt(pig_farm_staff_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_HASHID'
            }
        }
    
    pig_farm_staff_id = res[0]
    
    
    staff_user_hid  = data.staff_user_hid
    staff_user_id   = 0
    
    if staff_user_hid is not None:
        res = hashids_user.decrypt(uhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                    'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID'
                }
            }
        
        staff_user_id = res[0]
    
    

    data.name                = name
    data.user_id             = user_id
    data.pig_farm_id         = pig_farm_id
    data.pig_farm_staff_id   = pig_farm_staff_id
    data.staff_user_id       = staff_user_id
    
    res_update    =  model['pig_farm_staff'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_farm_staff']['id']
    res_update['pig_farm_staff']['hid'] = pig_farm_staff_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    

@app.get("/pig_farm_staff/delete", tags=["Pig Farm"])
async def pig_farm_staff_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_HASHID'
            }
        }
    
    pig_farm_staff_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_farm_staff_id':     pig_farm_staff_id
    }
    
    
    res_delete    =  model['pig_farm_staff'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_farm_staff']['id']
    res_delete['pig_farm_staff']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)
        
    return res_delete
    
    
@app.get("/pig_farm_staff/list", tags=["Pig Farm"])
async def pig_farm_staff_list(request: Request, pfhid: str, 
    inc_deleted: int = 0, inc_user_audit:int = 0):
    
    """
    Will get pig_farm_staff list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID'
            }
        }
    
    
    pig_farm_id = res[0]
        
    res = model['pig_farm_staff'].get_list(pig_farm_id, 
            inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pig_farm_staff']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_farm_staff']['id']
        cur_entry['pig_farm_staff']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['pig_farm_staff']['user_id']
        cur_hid = hashids_user.encrypt(cur_id)
        
        del cur_entry['pig_farm_staff']['user_id']
        cur_entry['pig_farm_staff']['user_hid']   = cur_hid
        
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
