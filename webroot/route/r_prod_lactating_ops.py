# August 29, 2025
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


@app.post("/prod_lactating_ops/update")
async def prod_lactating_ops_update(prod_lactating_ops_data: dm.DataProdLactatingOps):
    uhid    = prod_lactating_ops_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_LACTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_LACTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    prod_lactating_ops_hid = prod_lactating_ops_data.prod_lactating_ops_hid
    
    res = hashids_common.decrypt(prod_lactating_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_LACTATING_OPS_INVALID_HASHID,
                'code': 'ERROR_PROD_LACTATING_OPS_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    prod_lactating_ops_id = res[0]
    
    
    staff_hid = prod_lactating_ops_data.staff_hid
    staff_id  = None
        
    res = hashids_common.decrypt(staff_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PROD_LACTATING_OPS_INVALID_STAFF_HASHID,
                'code': 'ERROR_PROD_LACTATING_OPS_INVALID_STAFF_HASHID',
                'desc': ''
            }
        }
    
    staff_id = res[0]
    
    
    
    
    prod_lactating_ops_data.user_id   = user_id
    prod_lactating_ops_data.prod_lactating_ops_id = prod_lactating_ops_id
    
    res_update    =  model['prod_lactating_ops'].update(prod_lactating_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['prod_lactating_ops']['id']
    res_update['prod_lactating_ops']['hid'] = prod_lactating_ops_hid
        
    return res_update
    

@app.get("/prod_lactating_ops/list")
async def prod_lactating_ops_list(prod_hid: str, inc_user_audit:int = 0):
    """
    Will get prod_lactating_ops list.
    
    Parameters
    ----------
    
    prod_hid:str
        pig_production hashid

    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_LACTATING_OPS_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PROD_LACTATING_OPS_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['prod_lactating_ops'].get_list(pig_prod_id, inc_user_audit)
    
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
        cur_id  = cur_entry['prod_lactating_ops']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['prod_lactating_ops']['id']
        cur_entry['prod_lactating_ops']['hid']   = cur_hid
        
        acc_lactating_ops_id  = cur_entry['acc_lactating_ops']['id']
        acc_lactating_ops_hid = hashids_common.encrypt(acc_lactating_ops_id)
        
        del cur_entry['acc_lactating_ops']['id']
        cur_entry['acc_lactating_ops']['hid']   = acc_lactating_ops_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    