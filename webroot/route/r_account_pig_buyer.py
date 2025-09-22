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




    
@app.post("/account_pig_buyer/add")
async def account_pig_buyer_add(account_pig_buyer_data: dm.DataAccountPigBuyer):
    name    = account_pig_buyer_data.name
    uhid    = account_pig_buyer_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME',
                'desc': ''
            }
        }
        

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    account_pig_buyer_data.name      = name
    account_pig_buyer_data.user_id   = user_id
    
    res_add    =  model['account_pig_buyer'].add(account_pig_buyer_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    account_pig_buyer_id  = res_add['account_pig_buyer']['id']
    account_pig_buyer_hid = hashids_common.encrypt(account_pig_buyer_id)
    
    # remove plain id
    del res_add['account_pig_buyer']['id']
    res_add['account_pig_buyer']['hid'] = account_pig_buyer_hid

    return res_add
    

@app.post("/account_pig_buyer/update")
async def account_pig_buyer_update(account_pig_buyer_data: dm.DataAccountPigBuyer):
    name    = account_pig_buyer_data.name
    uhid    = account_pig_buyer_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    account_pig_buyer_hid = account_pig_buyer_data.account_pig_buyer_hid
    res = hashids_common.decrypt(account_pig_buyer_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID',
                'desc': ''
            }
        }
    
    account_pig_buyer_id = res[0]
    
    
    account_pig_buyer_data.name      = name
    account_pig_buyer_data.user_id   = user_id
    account_pig_buyer_data.account_pig_buyer_id = account_pig_buyer_id
    
    res_update    =  model['account_pig_buyer'].update(account_pig_buyer_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['account_pig_buyer']['id']
    res_update['account_pig_buyer']['hid'] = account_pig_buyer_hid
        
    return res_update
    

@app.get("/account_pig_buyer/delete")
async def account_pig_buyer_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID',
                'desc': ''
            }
        }
    
    account_pig_buyer_id = res[0]
    
    
    data = {
        'user_id':              user_id,
        'account_pig_buyer_id':   account_pig_buyer_id
    }
    
    
    res_delete    =  model['account_pig_buyer'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['account_pig_buyer']['id']
    res_delete['account_pig_buyer']['hid'] = ehid
        
    return res_delete
    

@app.get("/account_pig_buyer/list")
async def account_pig_buyer_list(ahid: str, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get account_pig_buyer list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
            
    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
        
    """
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['account_pig_buyer'].get_list(account_id, inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
            
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pig_buyer']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_buyer']['id']
        cur_entry['pig_buyer']['hid']   = cur_hid
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    
