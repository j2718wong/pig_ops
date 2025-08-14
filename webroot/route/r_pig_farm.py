# August 10, 2025
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


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0


  

@app.post("/pig_farm/add")
async def pig_farm_add(pig_farm_data: dm.DataPigFarm):
    name    = pig_farm_data.name
    uhid    = pig_farm_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_INVALID_NAME',
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
        'user_id':          user_id,
        'name':             name,
        
        'country_id':       pig_farm_data.country_id,
        'adrs_level_1_id':  pig_farm_data.adrs_level_1_id,
        'adrs_level_2_id':  pig_farm_data.adrs_level_2_id,
        'adrs_level_3_id':  pig_farm_data.adrs_level_3_id,
        'latitude':         pig_farm_data.latitude,
        'longitude':        pig_farm_data.longitude
    }
    
    
    res_add    =  model['pig_farm'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_farm_id     = res_add['pig_farm']['id']
    pig_farm_flag   = res_add['pig_farm']['flag']
        
    pig_farm_hashid = hashids_common.encrypt(pig_farm_id)
    
    if pig_farm_id == 0:
        pig_farm_hashid = ''
    
    # remove plain id
    del res_add['pig_farm']['id']
    res_add['pig_farm']['h_id'] = pig_farm_hashid

    result_num      = res_add['result']['num']
    
    if result_num == PIG_FARM_ADD_RES_NUM_SUCCESS:
        data = {
           'pig_farm_id':   pig_farm_id,
           'hashid':        pig_farm_hashid
        }
        res_update = model['pig_farm'].update_hashid(data)
        
    return res_add
    
    
@app.post("/pig_farm/update")
async def pig_farm_update(pig_farm_data: dm.DataPigFarm):
    name    = pig_farm_data.name
    uhid    = pig_farm_data.uhid
    
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
    
    
    pig_farm_hid = pig_farm_data.pig_farm_hid
    
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    pig_farm_id = res[0]
    
    
    data = {
        'user_id':          user_id,
        'pig_farm_id':      pig_farm_id,
        'name':             name,
        
        'country_id':       pig_farm_data.country_id,
        'adrs_level_1_id':  pig_farm_data.adrs_level_1_id,
        'adrs_level_2_id':  pig_farm_data.adrs_level_2_id,
        'adrs_level_3_id':  pig_farm_data.adrs_level_3_id,
        'latitude':         pig_farm_data.latitude,
        'longitude':        pig_farm_data.longitude
    }
    
    
    res_update    =  model['pig_farm'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_update['pig_farm']['id']
    res_update['pig_farm']['h_id'] = pig_farm_hid
        
    return res_update
    
    
@app.get("/pig_farm/list")
async def pig_farm_list(ahid : str):
    """
    Will get pig farm list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

        
    """
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res_get  = model['pig_farm'].get_pig_farm_list(account_id)
    
    if res_get is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
            
    return res_get
    

    