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





ACCOUNT_REGISTER_RES_NUM_SUCCESS        = 0


  

@app.post("/account/register")
async def account_register(account_data: dm.DataAccount):
    name    = account_data.name
    uhid    = account_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    
    data = {
        'name':             name,
        'user_id':          user_id
    }
    
    
    res_register    =  model['account'].register(data)
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_register['account']['id']
    account_flag    = res_register['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_register['account']['id']
    res_register['account']['h_id'] = account_hashid

    result_num      = res_register['result']['num']
    
    if result_num == ACCOUNT_REGISTER_RES_NUM_SUCCESS:
        data = {
           'account_id':    account_id,
           'hashid':        account_hashid
        }
        res_update = model['account'].update_hashid(data)
        
    return res_register
    
    
@app.post("/account/update")
async def account_update(account_data: dm.DataAccount):
    name    = account_data.name
    uhid    = account_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    
    data = {
        'name':             name,
        'user_id':          user_id
    }
    
    
    res_update      =  model['account'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_update['account']['id']
    account_flag    = res_update['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_update['account']['id']
    res_update['account']['h_id'] = account_hashid

        
    return res_update
    
 