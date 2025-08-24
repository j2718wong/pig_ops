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


ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS            = 0
ACCOUNT_REQUEST_APPROVE_ADD_USER_RES_NUM_SUCCESS    = 0

    
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
    
    acc_req_id          = res_add['account_request']['id']
    acc_req_status_id   = res_add['account_request']['status_id']
        
    acc_req_hashid      = hashids_common.encrypt(acc_req_id)
    
    # remove plain id
    del res_add['account_request']['id']
    res_add['account_request']['hid'] = acc_req_hashid

    result_num      = res_add['result']['num']
    
    if result_num == ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS:
        # Get account admin emails
        account_admins = model['account'].get_list_account_admin(account_id)
        
        print('\n\nACcount admins; account_id = %s' % account_id)
        pprint.pprint(account_admins)
        
        
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
    res_approve['account_request']['hid'] = account_request_hashid


    requesting_user_id      = res_approve['requesting_user']['id']
    requesting_user_email   = res_approve['requesting_user']['email']
    result_num              = res_approve['result']['num']
    
    del res_approve['requesting_user']
    
    
    if result_num == ACCOUNT_REQUEST_APPROVE_ADD_USER_RES_NUM_SUCCESS:

        test = 1
        # TODO send email to user
        
    return res_approve
    

