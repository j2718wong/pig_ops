# August 23, 2025
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

   
@app.post("/pig_farm_staff/add")
async def pig_farm_staff(pig_farm_staff_data: dm.DataPigFarmStaff):
    name    = pig_farm_staff_data.name
    uhid    = pig_farm_staff_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_farm_hid = pig_farm_staff_data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_PIG_FARM_HASHID',
                'desc': ''
            }
        }
       
    pig_farm_id = res[0]
   
    
    staff_user_hid  = pig_farm_staff_data.staff_user_hid
    staff_user_id   = 0
    
    if staff_user_hid is not None:
        res = hashids_user.decrypt(uhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                    'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID',
                    'desc': ''
                }
            }
        
        staff_user_id = res[0]
    
    
    
    pig_farm_staff_data.name            = name
    pig_farm_staff_data.user_id         = user_id
    pig_farm_staff_data.pig_farm_id     = pig_farm_id
    pig_farm_staff_data.staff_user_id   = staff_user_id
    
    res_add    =  model['pig_farm_staff'].add(pig_farm_staff_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    pig_farm_staff_id    = res_add['pig_farm_staff']['id']
    pig_farm_staff_hid   = hashids_common.encrypt(pig_farm_staff_id)
    
    # remove plain id
    del res_add['pig_farm_staff']['id']
    res_add['pig_farm_staff']['hid'] = pig_farm_staff_hid

        
    return res_add
    

@app.post("/pig_farm_staff/update")
async def pig_farm_staff_update(pig_farm_staff_data: dm.DataPigFarmStaff):
    name    = pig_farm_staff_data.name
    uhid    = pig_farm_staff_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_NAME',
                'desc': ''
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_farm_hid = pig_farm_staff_data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
        
    pig_farm_id = res[0]
    
    
    pig_farm_staff_hid = pig_farm_staff_data.pig_farm_staff_hid
    
    res = hashids_common.decrypt(pig_farm_staff_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_staff_id = res[0]
    
    
    staff_user_hid  = pig_farm_staff_data.staff_user_hid
    staff_user_id   = 0
    
    if staff_user_hid is not None:
        res = hashids_user.decrypt(uhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                    'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID',
                    'desc': ''
                }
            }
        
        staff_user_id = res[0]
    
    

    pig_farm_staff_data.name                = name
    pig_farm_staff_data.user_id             = user_id
    pig_farm_staff_data.pig_farm_id         = pig_farm_id
    pig_farm_staff_data.pig_farm_staff_id   = pig_farm_staff_id
    pig_farm_staff_data.staff_user_id       = staff_user_id
    
    res_update    =  model['pig_farm_staff'].update(pig_farm_staff_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_farm_staff']['id']
    res_update['pig_farm_staff']['hid'] = pig_farm_staff_hid
        
    return res_update
    

@app.get("/pig_farm_staff/delete")
async def pig_farm_staff_delete(uhid:str, pig_farm_staff_hid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(pig_farm_staff_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_staff_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_farm_staff_id':     pig_farm_staff_id
    }
    
    
    res_delete    =  model['pig_farm_staff'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['pig_farm_staff']['id']
    res_delete['pig_farm_staff']['hid'] = pig_farm_staff_hid
        
    return res_delete
    
    
@app.get("/pig_farm_staff/list")
async def pig_farm_staff_list(pfhid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig_farm_staff list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_FARM_STAFF_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    
    pig_farm_id = res[0]
        
    res = model['pig_farm_staff'].get_list(pig_farm_id, 
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
    
    

    