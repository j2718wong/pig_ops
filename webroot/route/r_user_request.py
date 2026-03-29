# August 9, 2025
# Jack Wong

import os
import sys
import pprint


import jwt

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


from r_a0_security_checks   import (check_if_valid_user_account,
                                    get_user_account_info)

from r_utils                import (replace_plain_ids_user_account,
                                    remove_database_null_description)
                                    
from r_user                 import create_access_token


    
@app.get("/user_request/join_account", tags=["User"])
async def user_request_join_account(request: Request, code:str = None):
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_REQUEST_INVALID_USER_HASHID,
                'code': 'ERROR_USER_REQUEST_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_access_code.decrypt(code)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_REQUEST_INVALID_ACCESS_CODE,
                'code': 'ERROR_USER_REQUEST_INVALID_ACCESS_CODE'
            }
        }
    
    access_code_id = res[0]
    
    
    
    
    data = {
        'access_code_id':   access_code_id,
        'user_id':          user_id
    }
    
    
    res_join    =  model['user_req'].join_account(data)
    
    if res_join is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Check if user has an account_id already
    if res_join['user']['account_id'] > 0:
        # Already has account
        
        
        # Get user_id and account info
        data_user_account = get_user_account_info(user_id)
                
                
        # Replace the user block
        del res_join['user']
        
        
        # With this block
        res_join['user_account'] = data_user_account
        replace_plain_ids_user_account(data_user_account)

        
        # Create JWT token
        user_hid = data_user_account['user']['user']['hid']
        access_token = create_access_token(data={"uhid": user_hid})
        
        
        res_join['bearer_token'] = access_token
        
        remove_database_null_description(res_join)
        
        return res_join
    
    
    del res_join['user']
    remove_database_null_description(res_join)
    
    return res_join
    
    
    

@app.post("/user_request/approve_join_acc", tags=["Account Details"])
async def user_request_approve_add_user(request: Request, data: dm.DataApproveUserReq):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_REQUEST_INVALID_USER_HASHID,
                'code': 'ERROR_USER_REQUEST_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    user_req_hid = data.user_req_hid
    
    res = hashids_common.decrypt(user_req_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_REQUEST_INVALID_HASHID,
                'code': 'ERROR_USER_REQUEST_INVALID_HASHID'
            }
        }
    
    user_request_id = res[0]
    
    
    pig_farm_id  = 0
    pig_farm_hid = data.pig_farm_hid
    
    if pig_farm_hid is not None:
        res = hashids_common.decrypt(pig_farm_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_USER_REQUEST_INVALID_HASHID,
                    'code': 'ERROR_USER_REQUEST_INVALID_HASHID'
                }
            }
        
        pig_farm_id = res[0]
        
    
    data.user_id            = user_id
    data.user_req_id        = user_request_id
    data.pig_farm_id        = pig_farm_id
    
    
    res_approve    =  model['user_req'].approve_join_account(data)
    
    if res_approve is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    cur_id  = res_approve['user_request']['id']
    cur_hid  = hashids_account.encrypt(user_request_id)
    
    # remove plain id
    del res_approve['user_request']['id']
    res_approve['user_request']['hid'] = cur_hid


    requesting_user_id      = res_approve['requesting_user']['id']
    requesting_user_email   = res_approve['requesting_user']['email']
    result_num              = res_approve['result']['num']
    
    del res_approve['requesting_user']
    
    
    if result_num == 0:

        test = 1
        # TODO send email to user
        
    return res_approve
    



@app.get("/user_request/list", tags=["User"])
async def user_request_list(request: Request, ahid: str):
    """
    Will get user request list.
    
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
                'num':  ERROR_USER_REQUEST_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_USER_REQUEST_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        
        
    res = model['user_req'].get_list(account_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'    
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['user_req']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['user_req']['id']
        cur_entry['user_req']['hid']   = cur_hid
   
        
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    

