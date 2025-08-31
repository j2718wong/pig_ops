# August 31, 2025
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


@app.post("/acc_lactating_ops/add")
async def acc_lactating_ops_add(acc_lactating_ops_data: dm.DataAccLactatingOps):
    name    = acc_lactating_ops_data.name
    uhid    = acc_lactating_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_NAME,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    num_days_since_birth = acc_lactating_ops_data.num_days_since_birth
    if num_days_since_birth < 0 and num_days_since_birth > 115:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_NUMDAYS,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_NUMDAYS',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    acc_lactating_ops_data.name      = name
    acc_lactating_ops_data.user_id   = user_id
    
    res_add    =  model['acc_lactating_ops'].add(acc_lactating_ops_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    acc_gest_ops_id     = res_add['acc_lactating_ops']['id']
    acc_gest_ops_hid    = hashids_common.encrypt(acc_gest_ops_id)
    
    # remove plain id
    del res_add['acc_lactating_ops']['id']
    res_add['acc_lactating_ops']['hid'] = acc_gest_ops_hid

        
    return res_add
    

@app.post("/acc_lactating_ops/update")
async def acc_lactating_ops_update(acc_lactating_ops_data: dm.DataAccLactatingOps):
    name    = acc_lactating_ops_data.name
    uhid    = acc_lactating_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_NAME,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    num_days_since_birth = acc_lactating_ops_data.num_days_since_birth
    if num_days_since_birth < 0 and num_days_since_birth > 115:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_NUMDAYS,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_NUMDAYS',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    acc_lact_ops_hid = acc_lactating_ops_data.acc_lact_ops_hid
    
    
    res = hashids_common.decrypt(acc_lact_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    acc_lact_ops_id = res[0]
    
    
    acc_lactating_ops_data.name      = name
    acc_lactating_ops_data.user_id   = user_id
    acc_lactating_ops_data.acc_lact_ops_id = acc_lact_ops_id
    
    res_update    =  model['acc_lactating_ops'].update(acc_lactating_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['acc_lactating_ops']['id']
    res_update['acc_lactating_ops']['hid'] = acc_lact_ops_hid
        
    return res_update
    
    
@app.get("/acc_lactating_ops/delete")
async def acc_lactating_ops_delete(uhid:str, acc_lactating_ops_hid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(acc_lactating_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_HASHID',
                'desc': ''
            }
        }
    
    acc_lactating_ops_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'acc_lactating_ops_id': acc_lactating_ops_id
    }
    
    
    res_delete    =  model['acc_lactating_ops'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['acc_lactating_ops']['id']
    res_delete['acc_lactating_ops']['hid'] = acc_lactating_ops_hid
        
    return res_delete
    
    
@app.get("/acc_lactating_ops/list")
async def acc_lactating_ops_list(ahid: str, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get acc_lactating_ops list.
    
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
                'num':  ERROR_ACC_LACTATING_OPS_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACC_LACTATING_OPS_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['acc_lactating_ops'].get_list(account_id,
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
    
    

    