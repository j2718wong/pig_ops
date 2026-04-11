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
from r_utils                import remove_database_null_description



   
@app.post("/pig_prod_notes/add", tags=["Production Details"])
async def pig_prod_notes_add(request: Request, data: dm.DataPigProdNotes):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    if data.date_notes is None:
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d')
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_prod_id     = 0
    sow_boar_id     = 0
    
    pig_prod_hid    = data.pig_prod_hid
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_id = res[0]
    
    
    sow_boar_hid    = data.sow_boar_hid
    
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_NOTES_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_NOTES_INVALID_SOW_BOAR_HASHID'
                }
            }
        
        sow_boar_id = res[0]
    
    
    # check valid keys
    if sow_boar_id == 0 and pig_prod_id == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_NO_VALID_KEY,
                'code': 'ERROR_PIG_PROD_NOTES_NO_VALID_KEY'
            }
        }
    
    data.user_id     = user_id
    data.pig_prod_id = pig_prod_id
    data.sow_boar_id = sow_boar_id
    
    res_add    =  model['prod_notes'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['pig_prod_notes']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['pig_prod_notes']['id']
    res_add['pig_prod_notes']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    

@app.post("/pig_prod_notes/update", tags=["Production Details"])
async def pig_prod_notes_update(request: Request, data: dm.DataPigProdNotes):
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
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_prod_notes_hid = data.pig_prod_notes_hid
    
    res = hashids_common.decrypt(pig_prod_notes_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_HASHID'
            }
        }
    
    
    pig_prod_notes_id = res[0]
    
    
    data.user_id   = user_id
    data.pig_prod_notes_id = pig_prod_notes_id
    
    res_update    =  model['prod_notes'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_notes']['id']
    res_update['pig_prod_notes']['hid'] = pig_prod_notes_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    
    return res_update
    

@app.get("/pig_prod_notes/delete", tags=["Production Details"])
async def pig_prod_notes_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_HASHID'
            }
        }
    
    pig_prod_notes_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_prod_notes_id':     pig_prod_notes_id
    }
    
    
    res_delete    =  model['pig_prod_notes'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_prod_notes']['id']
    res_delete['pig_prod_notes']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)
    
    
    return res_delete
    
    
def get_data_pig_prod_notes(pig_prod_id = 0, sow_boar_id = 0, 
        inc_deleted = 0, inc_user_audit = 0):
            
    res = model['prod_notes'].get_list(
        pig_prod_id     = pig_prod_id, 
        sow_boar_id     = sow_boar_id, 
        inc_deleted     = inc_deleted, 
        inc_user_audit  = inc_user_audit)
    
    if res is None:
        return None
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['prod_notes']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['prod_notes']['id']
        cur_entry['prod_notes']['hid']   = cur_hid

        
        if 'pig_medvac' in cur_entry:
            cur_id  = cur_entry['pig_medvac']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['id']
            cur_entry['pig_medvac']['hid']   = cur_hid
    
    
    return res
    
    
    
@app.get("/pig_prod_notes/list", tags=["Production Details"])
async def pig_prod_notes_list(request: Request, pig_prod_hid: str = None, 
        sow_boar_hid: str = None,  
        inc_deleted: int = 0, inc_user_audit:int = 0):
    
    """
    Will get pig_prod_notes list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod_hid hashid

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
    
    
    pig_prod_id     = 0
    sow_boar_id     = 0
    
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID'
                }
            }
            
        pig_prod_id = res[0]
        
        
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_NOTES_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_NOTES_INVALID_SOW_BOAR_HASHID'
                }
            }
        
        sow_boar_id = res[0]
    
    
        
    res = get_data_pig_prod_notes(pig_prod_id, sow_boar_id, 
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
            'num':  0
        },
        
        'data': res
    }
    
    

    
