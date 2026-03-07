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


FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4



    
@app.get("/user_request/join_account", tags=["User"])
async def user_request_join_account(request: Request, ahid:str = None):
    
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
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_REQUEST_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_USER_REQUEST_INVALID_ACCOUNT_HASHID'
            }
        }
    
    account_id = res[0]
    
    
    
    data = {
        'account_id':       account_id,
        'user_id':          user_id
    }
    
    
    res_add    =  model['user_req'].join_account(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    user_req_id         = res_add['user_request']['id']
    user_req_status_id  = res_add['user_request']['status_id']
      
    # Replace Plain Id
    cur_id              = user_req_id
    cur_hid             = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['user_request']['id']
    res_add['user_request']['hid'] = cur_hid


    result_num      = res_add['result']['num']
    
    if result_num == 0:
        # Get account admin emails
        account_admins = model['account'].get_list_account_admin(account_id)
        
        print('\n\nACcount admins; account_id = %s' % account_id)
        pprint.pprint(account_admins)
        
        
        # TODO send email notification to account_admins
        
        # TODO send email to user
        
    return res_add
    

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
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    

