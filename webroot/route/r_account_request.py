# August 9, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4


ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS        = 0

    
@app.get("/account_request/add_user")
async def account_request_add_user(uhid: str, ahid:str):
        
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_REQUEST_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_REQUEST_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_REQUEST_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_REQUEST_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    account_id = res[0]
    
    
    
    data = {
        'account_id':       account_id,
        'user_id':          user_id
    }
    
    
    res_add    =  model['acc_req'].add_user(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_add['account']['id']
    account_flag    = res_add['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_add['account']['id']
    res_add['account']['h_id'] = account_hashid

    result_num      = res_add['result']['num']
    
    if result_num == ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS:
        # Get account admin emails
        account_admins = model['account'].get_account_admin(account_id)
        
        
        
        # TODO send email notification to account_admins
        
        # TODO send email to user
        
    return res_add
    

@app.get("/account_request/approve_add_user")
async def account_request_approve_add_user(arhid: str, uhid:str):
        
    res = hashids_common.decrypt(arhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_REQUEST_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_REQUEST_INVALID_HASHID',
                'desc': ''
            }
        }
    
    acc_request_id = res[0]
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_REQUEST_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_REQUEST_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    
    data = {
        'acc_request_id':       acc_request_id,
        'approving_user_id':    user_id
    }
    
    
    res_approve    =  model['acc_req'].approve_add_user(data)
    
    if res_approve is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    account_request_id  = res_approve['account_request']['id']
    account_request_hashid  = hashids_account.encrypt(account_request_id)
    
    # remove plain id
    del res_approve['account_request']['id']
    res_approve['account_request']['h_id'] = account_request_hashid

    result_num      = res_approve['result']['num']
    
    if result_num == ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS:
        # Get account admin emails
        account_admins = model['account'].get_account_admin(account_id)
        
        
        
        # TODO send email notification to account_admins
        
        # TODO send email to user
        
    return res_add
    

