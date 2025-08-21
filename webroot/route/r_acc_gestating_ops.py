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

    
@app.post("/acc_gestating_ops/add")
async def acc_gestating_ops_add(acc_gestating_ops_data: dm.DataAccGestatingOps):
    name    = acc_gestating_ops_data.name
    uhid    = acc_gestating_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_NAME,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    num_days_since_insem = acc_gestating_ops_data.num_days_since_insem
    if num_days_since_insem < 0 and num_days_since_insem > 115:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_NUMDAYS,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_NUMDAYS',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    acc_gestating_ops_data.name      = name
    acc_gestating_ops_data.user_id   = user_id
    
    res_add    =  model['acc_gestating_ops'].add(acc_gestating_ops_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    acc_gest_ops_id     = res_add['acc_gestating_ops']['id']
    acc_gest_ops_hid    = hashids_common.encrypt(acc_gest_ops_id)
    
    # remove plain id
    del res_add['acc_gestating_ops']['id']
    res_add['acc_gestating_ops']['h_id'] = acc_gest_ops_hid

        
    return res_add
    

@app.post("/acc_gestating_ops/update")
async def acc_gestating_ops_update(acc_gestating_ops_data: dm.DataAccGestatingOps):
    name    = acc_gestating_ops_data.name
    uhid    = acc_gestating_ops_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_NAME,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    num_days_since_insem = acc_gestating_ops_data.num_days_since_insem
    if num_days_since_insem < 0 and num_days_since_insem > 115:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_NUMDAYS,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_NUMDAYS',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    acc_gest_ops_hid = acc_gestating_ops_data.acc_gest_ops_hid
    
    
    res = hashids_common.decrypt(acc_gest_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_HASHID',
                'desc': ''
            }
        }
    
    
    acc_gest_ops_id = res[0]
    
    
    acc_gestating_ops_data.name      = name
    acc_gestating_ops_data.user_id   = user_id
    acc_gestating_ops_data.acc_gest_ops_id = acc_gest_ops_id
    
    res_update    =  model['acc_gestating_ops'].update(acc_gestating_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['acc_gestating_ops']['id']
    res_update['acc_gestating_ops']['h_id'] = acc_gest_ops_hid
        
    return res_update
    
    
@app.get("/acc_gestating_ops/list")
async def acc_gestating_ops_list(ahid: str):
    """
    Will get acc_gestating_ops list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

        
    """
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['acc_gestating_ops'].get_acc_gestating_ops_list(account_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    