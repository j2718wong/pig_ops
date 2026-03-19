# March 19, 2025
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



    
@app.post("/access_code/add", tags=["Account"])
async def account_access_code_add(request: Request, data: dm.DataAccountAccessCode):
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
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    


    data.user_id            = user_id

    
    res_add    =  model['access_code'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id      = res_add['access_code']['id']
    cur_hid     = hashids_access_code.encrypt(cur_id)
    
    # remove plain id
    del res_add['access_code']['id']
    res_add['access_code']['hid'] = cur_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)


    return res_add
    

@app.post("/access_code/update", tags=["Account"])
async def account_access_code_update(request: Request, data: dm.DataAccountAccessCode):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    


    access_code_hid = data.access_code_hid
    res = hashids_access_code.decrypt(access_code_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_HASHID'
            }
        }
    
    access_code_id = res[0]
    
    
    
    user_group_hid = data.user_group_hid
    res = hashids_common.decrypt(user_group_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_USERGROUP_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_USERGROUP_HASHID'
            }
        }
    
    user_group_id = res[0]
    
    
    
    
    
    
    
    data.user_id            = user_id
    data.access_code_id     = access_code_id
    data.user_group_id      = user_group_id
    
    
    res_update    =  model['access_code'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['account_access_code']['id']
    res_update['account_access_code']['hid'] = account_access_code_hid
        
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update
    

@app.get("/access_code/delete", tags=["Account"])
async def account_access_code_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_USER_HASHID'
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
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_HASHID'
            }
        }
    
    account_access_code_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'account_access_code_id':   account_access_code_id
    }
    
    
    res_delete    =  model['account_access_code'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['account_access_code']['id']
    res_delete['account_access_code']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)

    
    return res_delete
    

@app.get("/access_code/list", tags=["Account"])
async def account_access_code_list(request: Request, ahid: str):
    """
    Will get account_access_code list.
    
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
                'num':  ERROR_ACCOUNT_ACCESS_CODE_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_ACCESS_CODE_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        
    res = model['access_code'].get_list(account_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
            
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['access_code']['id']
        cur_hid = hashids_access_code.encrypt(cur_id)
        
        del cur_entry['access_code']['id']
        cur_entry['access_code']['hid']   = cur_hid
        
        
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    
