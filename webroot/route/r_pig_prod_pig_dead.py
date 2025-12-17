# August 23, 2025
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


@app.get("/pig_dead_type/list", tags=["Production Details"])
async def pig_dead_type_list():
    """
    Will get feed_type list.
    
    Parameters
    ----------
    
   
    """
    
        
    res = model['prod_pig_dead'].get_pig_dead_type_list()
    
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

   
@app.post("/prod_pig_dead/add", tags=["Production Details"])
async def prod_pig_dead_add(prod_pig_dead_data: dm.DataPigProdDeadPig):
    uhid    = prod_pig_dead_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid        = prod_pig_dead_data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = prod_pig_dead_data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_DEAD_INVALID_PROD_GROUP_HASHID,
                    'code': 'ERROR_PIG_DEAD_INVALID_PROD_GROUP_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_group_hid = res[0]
    
    
    pig_dead_type_hid   = prod_pig_dead_data.pig_dead_type_hid
    pig_dead_type_id    = 0
    
    res = hashids_common.decrypt(pig_dead_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_PIG_DEAD_TYPE_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_PIG_DEAD_TYPE_HASHID',
                'desc': ''
            }
        }
    
    pig_dead_type_id = res[0]
    
    
    prod_pig_dead_data.user_id          = user_id
    prod_pig_dead_data.pig_prod_id      = pig_prod_id
    prod_pig_dead_data.pig_prod_group_id= pig_prod_group_id
    prod_pig_dead_data.pig_dead_type_id = pig_dead_type_id
    
    res_add    =  model['prod_pig_dead'].add(prod_pig_dead_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    prod_pig_dead_id    = res_add['prod_pig_dead']['id']
    prod_pig_dead_hid   = hashids_common.encrypt(prod_pig_dead_id)
    
    # remove plain id
    del res_add['prod_pig_dead']['id']
    res_add['prod_pig_dead']['hid'] = prod_pig_dead_hid

        
    return res_add
    

@app.post("/prod_pig_dead/update", tags=["Production Details"])
async def prod_pig_dead_update(prod_pig_dead_data: dm.DataPigProdDeadPig):
    uhid    = prod_pig_dead_data.uhid
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    

    prod_pig_dead_hid = prod_pig_dead_data.prod_pig_dead_hid
    
    res = hashids_common.decrypt(prod_pig_dead_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    prod_pig_dead_id = res[0]
    
    
    prod_pig_dead_data.user_id   = user_id
    prod_pig_dead_data.prod_pig_dead_id = prod_pig_dead_id
    
    res_update    =  model['prod_pig_dead'].update(prod_pig_dead_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['prod_pig_dead']['id']
    res_update['prod_pig_dead']['hid'] = prod_pig_dead_hid
        
    return res_update
    
  
@app.get("/prod_pig_dead/list", tags=["Production Details"])
async def prod_pig_dead_list(pig_prod_hid: str):
    """
    Will get prod_pig_dead list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pir_prod hashid

    
    
    """
    
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_DEAD_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['prod_pig_dead'].get_list(pig_prod_id)
    
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
        cur_id  = cur_entry['pig_dead']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_dead']['id']
        cur_entry['pig_dead']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['pig_dead']['dead_type_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_dead']['dead_type_id']
        cur_entry['pig_dead']['dead_type_hid']   = cur_hid
        
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    