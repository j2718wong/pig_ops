# August 9, 2025
# Jack Wong

import os
import sys
import pprint


import jwt

from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse
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


from r_a0_security_checks   import (check_if_valid_user_account,
                                    get_user_account_info)

from r_utils                import (get_location_address_names_and_replace_ids,
                                    replace_plain_ids_account,
                                    replace_plain_ids_user_account,
                                    remove_database_null_description)


ACCOUNT_REGISTER_RES_NUM_SUCCESS        = 0


    

@app.get("/account/info", tags=["Account"])
async def user_account_info(request: Request, ahid: str):
    """
    Will get account info

    Parameters
    ----------
    ahid : str
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
                'num':  ERROR_ACCOUNT_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_HASHID'
            }
        }
    
    account_id = res[0]
    
    
    res = model['account'].get_info(account_id)
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    replace_plain_ids_account(res)
    
        
    result = {
            'result':{
                'num':  0
            }
        }
        
    result = result | res
    
    return result
        
        
        


@app.post("/account/register", tags=["Account"])
async def account_register(request: Request, account_data: dm.DataAccount):
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    
    name    = account_data.name
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

    
    account_data.name       = name 
    account_data.user_id    = user_id
    
    res_register    =  model['account'].register(account_data)
    
    
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    account_id      = res_register['account']['id']
    account_flag    = res_register['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_register['account']['id']
    res_register['account']['hid'] = account_hashid

    result_num      = res_register['result']['num']
    
    if result_num == ACCOUNT_REGISTER_RES_NUM_SUCCESS:
        data = {
           'account_id':    account_id,
           'hashid':        account_hashid
        }
        res_update = model['account'].update_hashid(data)
        
        
    # This will return user and account info
    data_user_account = get_user_account_info(user_id)
    
    
    
    # Remove not useful data
    del data_user_account['account']['settings_operations']
    del data_user_account['account']['account']['current_bill']
    

    
    # replace the account block
    del res_register['account']
    
    
    # with this block
    res_register['user_account'] = data_user_account


    replace_plain_ids_user_account(data_user_account)

        
    return res_register
    

@app.get("/user_account", tags=["Account"])
async def user_account(request: Request):
    """
    Will get user_account info

    Parameters
    ----------


    
    """
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    
    user_id = res[0]


    # This will return user and account info
    data_user_account = get_user_account_info(user_id)
    
    
    
    # Remove not useful data
    del data_user_account['account']['settings_operations']
    del data_user_account['account']['account']['current_bill']
    
    
    replace_plain_ids_user_account(data_user_account)

    return {
        'result':{
            'num':  0
        },
        
        'user_account': data_user_account
    }

    
@app.post("/account/update", tags=["Account"])
async def account_update(request: Request, account_data: dm.DataAccount):
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    name    = account_data.name
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
                'num':  ERROR_ACCOUNT_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_USER_HASHID'
            }
        }
    
    
    user_id = res[0]
    
    account_data.name       = name 
    account_data.user_id    = user_id
        
    res_update      =  model['account'].update(account_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    account_id      = res_update['account']['id']
    
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    
    if data_account is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': 'Cannot read account'
            }
        }
    
    replace_plain_ids_account(data_account)
    
    
    # Remove account block in res_update
    del res_update['account']
    
    # Replace with data_account
    res_update['account'] = data_account['account']
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    
    
@app.post("/account/update_settings", tags=["Account"])
async def account_update_settings(request: Request, data: dm.DataAccountSettings):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_USER_HASHID'
            }
        }
    
    
    user_id = res[0]
    
    data.user_id    = user_id
        
    res_update      =  model['account'].update_settings(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
        
    return res_update



@app.get("/account/data_ver_num", tags=["Account"])
async def account_data_ver_num(request: Request, ahid: str, r: int = 0):
    """
    Will get account data_ver_num.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
    
    r : int
        return type; 0 = json object; 1 = array of integers
        
        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_account.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_HASHID'
            }
        }
    
    
    account_id = res[0]
        
        
    return_array = 0
    if r > 0:
        return_array = 1

    res = model['account'].get_data_ver_num(account_id, return_array)

    
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
    
