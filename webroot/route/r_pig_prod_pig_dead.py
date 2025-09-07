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

   
@app.post("/prod_pig_dead/add")
async def pig_prod_pig_dead_add(pig_prod_pig_dead_data: dm.DataPigProdDeadPig):
    uhid    = pig_prod_pig_dead_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_DEAD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid        = pig_prod_pig_dead_data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = pig_prod_pig_dead_data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_group_hid = res[0]
    
    
    
    pig_prod_pig_dead_data.user_id          = user_id
    pig_prod_pig_dead_data.pig_prod_id      = pig_prod_id
    pig_prod_pig_dead_data.pig_prod_group_id= pig_prod_group_id
    
    res_add    =  model['prod_pig_dead'].add(pig_prod_pig_dead_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    pig_prod_pig_dead_id    = res_add['pig_prod_pig_dead']['id']
    pig_prod_pig_dead_hid   = hashids_common.encrypt(pig_prod_pig_dead_id)
    
    # remove plain id
    del res_add['pig_prod_pig_dead']['id']
    res_add['pig_prod_pig_dead']['hid'] = pig_prod_pig_dead_hid

        
    return res_add
    

@app.post("/prod_pig_dead/update")
async def pig_prod_pig_dead_update(pig_prod_pig_dead_data: dm.DataPigProdDeadPig):
    uhid    = pig_prod_pig_dead_data.uhid
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_DEAD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    

    pig_prod_pig_dead_hid = pig_prod_pig_dead_data.pig_prod_pig_dead_hid
    
    res = hashids_common.decrypt(pig_prod_pig_dead_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_DEAD_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_DEAD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_pig_dead_id = res[0]
    
    
    pig_prod_pig_dead_data.user_id   = user_id
    pig_prod_pig_dead_data.pig_prod_pig_dead_id = pig_prod_pig_dead_id
    
    res_update    =  model['prod_pig_dead'].update(pig_prod_pig_dead_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_pig_dead']['id']
    res_update['pig_prod_pig_dead']['hid'] = pig_prod_pig_dead_hid
        
    return res_update
    
  
@app.get("/pig_prod_pig_dead/list")
async def pig_prod_pig_dead_list(ahid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig_prod_pig_dead list.
    
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
                'num':  ERROR_PIG_PROD_PIG_DEAD_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_DEAD_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['pig_prod_pig_dead'].get_list(account_id, 
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
        
        cur_pig_race_id  = cur_entry['pig_race']['id']
        cur_pig_race_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_race']['id']
        cur_entry['pig_race']['hid']   = cur_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    