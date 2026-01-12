# January 12, 2025
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

   
@app.post("/pig_medvac/add", tags=["Pig Details"])
async def pig_medvac_add(pig_race_line_data: dm.DataPigRaceLine):
    name    = pig_race_line_data.name
    uhid    = pig_race_line_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_NAME,
                'code': 'ERROR_PIG_MEDVAC_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_race_line_data.name      = name
    pig_race_line_data.user_id   = user_id
    
    res_add    =  model['pig_race_line'].add(pig_race_line_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    pig_race_line_id    = res_add['pig_race_line']['id']
    pig_race_line_hid   = hashids_common.encrypt(pig_race_line_id)
    
    # remove plain id
    del res_add['pig_race_line']['id']
    res_add['pig_race_line']['hid'] = pig_race_line_hid

        
    return res_add
    

@app.post("/pig_medvac/update", tags=["Pig Details"])
async def pig_medvac_update(pig_race_line_data: dm.DataPigRaceLine):
    name    = pig_race_line_data.name
    uhid    = pig_race_line_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_NAME,
                'code': 'ERROR_PIG_MEDVAC_INVALID_NAME'
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_race_line_hid = pig_race_line_data.pig_race_line_hid
    
    res = hashids_common.decrypt(pig_race_line_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_HASHID,
                'code': 'ERROR_PIG_MEDVAC_HASHID'
            }
        }
    
    
    pig_race_line_id = res[0]
    
    
    pig_race_line_data.name      = name
    pig_race_line_data.user_id   = user_id
    pig_race_line_data.pig_race_line_id = pig_race_line_id
    
    res_update    =  model['pig_race_line'].update(pig_race_line_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_race_line']['id']
    res_update['pig_race_line']['hid'] = pig_race_line_hid
        
    return res_update
    

@app.get("/pig_medvac/delete", tags=["Pig Details"])
async def pig_medvac_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_HASHID'
            }
        }
    
    pig_race_line_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_race_line_id':     pig_race_line_id
    }
    
    
    res_delete    =  model['pig_race_line'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_race_line']['id']
    res_delete['pig_race_line']['hid'] = ehid
        
    return res_delete
    
    
@app.get("/pig_medvac/list", tags=["Pig Details"])
async def pig_medvac_list(sow_boar_hid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig medvac list.
    
    Parameters
    ----------
    
    sow_boar_hid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_SOW_BOAR_HASHID,
                'code': 'ERROR_PIG_MEDVAC_SOW_BOAR_HASHID'
            }
        }
    
    
    sow_boar_id = res[0]
        
    res = model['pig_medvac'].get_list(sow_boar_id, 
            inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['medvac']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['id']
        cur_entry['medvac']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['brand']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['brand']['id']
        cur_entry['medvac']['brand']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['type']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['type']['id']
        cur_entry['medvac']['type']['hid']   = cur_hid
        
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    