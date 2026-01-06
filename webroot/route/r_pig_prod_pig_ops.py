# August 29, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


@app.post("/pig_prod_pig_ops/update", tags=["Production Details"])
async def pig_prod_pig_ops_update(pig_prod_pig_ops_data: dm.DataPigProdPigOps):
    uhid    = pig_prod_pig_ops_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_pig_prod_pig_ops_INVALID_USER_HASHID,
                'code': 'ERROR_pig_prod_pig_ops_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_pig_ops_hid = pig_prod_pig_ops_data.pig_prod_pig_ops_hid
    
    res = hashids_common.decrypt(pig_prod_pig_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_pig_prod_pig_ops_INVALID_HASHID,
                'code': 'ERROR_pig_prod_pig_ops_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_pig_ops_id = res[0]
    
    
    staff_hid = pig_prod_pig_ops_data.staff_hid
    staff_id  = None
    
    # Needs staff info if not done_by_user
    if pig_prod_pig_ops_data.done_by_user == 0:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_pig_prod_pig_ops_INVALID_STAFF_HASHID,
                    'code': 'ERROR_pig_prod_pig_ops_INVALID_STAFF_HASHID',
                    'desc': ''
                }
            }
        
        staff_id = res[0]
        
    
    pig_prod_pig_ops_data.user_id               = user_id
    pig_prod_pig_ops_data.pig_prod_pig_ops_id   = pig_prod_pig_ops_id
    pig_prod_pig_ops_data.staff_id              = staff_id
    
    res_update    =  model['pig_prod_pig_ops'].update(pig_prod_pig_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_pig_ops']['id']
    res_update['pig_prod_pig_ops']['hid'] = pig_prod_pig_ops_hid
        
        
    if 'added_new_staff' in res_update:
        # Get new staff list fo refresh client staff_list
        
        pig_farm_id = res_update['pig_farm_id']
        del res_update['pig_farm_id']
        del res_update['added_new_staff']
        list_staff = model['pig_farm_staff'].get_list(pig_farm_id, minimum_info = 1)
        
        if list_staff is not None:
            for cur_entry in list_staff:
                cur_id      = cur_entry['pig_farm_staff']['id']
                cur_hid     = hashids_common.encrypt(cur_id)
            
                del cur_entry['pig_farm_staff']['id']
                cur_entry['pig_farm_staff']['hid']   = cur_hid
            
            res_update['staff_list'] = list_staff
            
        
    return res_update
    

@app.get("/pig_prod_pig_ops/list", tags=["Production Details"])
async def pig_prod_pig_ops_list(prod_hid: str, operation_type: int, inc_user_audit:int = 0):
    """
    Will get pig_prod_pig_ops list.
    
    Parameters
    ----------
    
    prod_hid:str
        pig_production hashid

    operation_type :int
        1 = GESTATING; 2 = LACTATING; 3 = GROWING
        
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_pig_prod_pig_ops_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_pig_prod_pig_ops_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['pig_prod_pig_ops'].get_list(pig_prod_id, operation_type, 
        inc_user_audit)
    
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
        cur_id  = cur_entry['pig_prod_pig_ops']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_prod_pig_ops']['id']
        cur_entry['pig_prod_pig_ops']['hid']   = cur_hid
        
        acc_gestating_ops_id  = cur_entry['account_pig_ops']['id']
        acc_gestating_ops_hid = hashids_common.encrypt(acc_gestating_ops_id)
        
        del cur_entry['account_pig_ops']['id']
        cur_entry['account_pig_ops']['hid']   = acc_gestating_ops_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    