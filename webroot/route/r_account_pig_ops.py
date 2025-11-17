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




PIG_OPERATION_TYPES = [
    PIG_OPERATION_TYPE_GESTATING,
    PIG_OPERATION_TYPE_LACTATING_PIGLETS,
    PIG_OPERATION_TYPE_GROWING
]


    
@app.post("/account_pig_ops/add")
async def account_pig_ops_add(account_pig_ops_data: dm.DataAccountPigOps):
    name    = account_pig_ops_data.name
    uhid    = account_pig_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    operation_type  = account_pig_ops_data.operation_type
    
    if operation_type not in PIG_OPERATION_TYPES:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE',
                'desc': ''
            }
        }
        

    num_days_since = account_pig_ops_data.num_days_since
    
    if operation_type == PIG_OPERATION_TYPE_GESTATING:
        if num_days_since < 0 and num_days_since > 115:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
            
    
    if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
        if num_days_since < 0 and num_days_since > 45:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    if operation_type == PIG_OPERATION_TYPE_GROWING:
        if num_days_since < 0 and num_days_since > 300:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    account_pig_ops_data.name      = name
    account_pig_ops_data.user_id   = user_id
    
    res_add    =  model['account_pig_ops'].add(account_pig_ops_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    account_pig_ops_id  = res_add['account_pig_ops']['id']
    account_pig_ops_hid = hashids_common.encrypt(account_pig_ops_id)
    
    # remove plain id
    del res_add['account_pig_ops']['id']
    res_add['account_pig_ops']['hid'] = account_pig_ops_hid

    return res_add
    

@app.post("/account_pig_ops/update")
async def account_pig_ops_update(account_pig_ops_data: dm.DataAccountPigOps):
    name    = account_pig_ops_data.name
    uhid    = account_pig_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    operation_type  = account_pig_ops_data.operation_type
    
    if operation_type not in PIG_OPERATION_TYPES:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE',
                'desc': ''
            }
        }
        

    num_days_since = account_pig_ops_data.num_days_since
    
    if operation_type == PIG_OPERATION_TYPE_GESTATING:
        if num_days_since < 0 and num_days_since > 115:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
            
    
    if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
        if num_days_since < 0 and num_days_since > 45:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    if operation_type == PIG_OPERATION_TYPE_GROWING:
        if num_days_since < 0 and num_days_since > 300:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    account_pig_ops_hid = account_pig_ops_data.account_pig_ops_hid
    res = hashids_common.decrypt(account_pig_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID',
                'desc': ''
            }
        }
    
    account_pig_ops_id = res[0]
    
    
    account_pig_ops_data.name      = name
    account_pig_ops_data.user_id   = user_id
    account_pig_ops_data.account_pig_ops_id = account_pig_ops_id
    
    res_update    =  model['account_pig_ops'].update(account_pig_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['account_pig_ops']['id']
    res_update['account_pig_ops']['hid'] = account_pig_ops_hid
        
    return res_update
    

@app.get("/account_pig_ops/delete")
async def account_pig_ops_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID',
                'desc': ''
            }
        }
    
    account_pig_ops_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'account_pig_ops_id':   account_pig_ops_id
    }
    
    
    res_delete    =  model['account_pig_ops'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['account_pig_ops']['id']
    res_delete['account_pig_ops']['hid'] = ehid
        
    return res_delete
    

@app.get("/account_pig_ops/list")
async def account_pig_ops_list(ahid: str, operation_type: int, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get account_pig_ops list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
        
    operation_type :int
        1 = GESTATING; 2 = LACTATING_PIGLETS; 3 = LACTATING_SOW
    
    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
        
    """
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['account_pig_ops'].get_list(account_id, operation_type,
            inc_deleted, inc_user_audit)
    
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
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    
